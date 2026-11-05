"""MongoDB storage: one document per teacher.

{
    "lastname", "name", "father",   # normalized (upper case, no accents), latest spelling
    "names": every spelling seen, eg. ΝΙΚΟΛΕΤΤΑ in 2023 and ΝΙΚΟΛΕΤΑ in 2026,
    "adt":  current ID,
    "adts": every ID ever seen for this teacher,
    "specializations": [...],
    "rankings": [ one entry per ranking list row (2GE/2EA, year, spec, am) ],
    "hires":    [ one entry per hire (school_year, round, spec) ],
    "review":   [ notes for a human when a match was ambiguous ],
}
"""

import os
import re
import unicodedata

from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://mongo:27017")
MONGO_DB = os.environ.get("MONGO_DB", "ekpedeutikoi")

# Current-format ADT: one Greek letter followed by 8 digits (eg. Α00576786).
# Older files use letters followed by 6 digits (eg. ΑΙ519314).
NEW_ADT_PATTERN = re.compile(r"^[Α-Ω]\d{8}$")


def get_teachers(client=None):
    teachers = (client or MongoClient(MONGO_URL))[MONGO_DB]["teachers"]
    teachers.create_index("adts")
    teachers.create_index("names")
    return teachers


def normalize(value):
    """'Άννα  Μαρία' / ['ΆΝΝΑ', 'ΜΑΡΙΑ'] -> 'ΑΝΝΑ ΜΑΡΙΑ'"""
    if isinstance(value, list):
        value = " ".join(value)
    value = unicodedata.normalize("NFD", str(value or "").upper())
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    return " ".join(value.split())


def valid_adt(adt):
    adt = str(adt or "").strip()
    return len(adt) >= 5 and any(c.isdigit() for c in adt)


def _person(row):
    return {
        "lastname": normalize(row["lastname"]),
        "name": normalize(row["name"]),
        "father": normalize(row["father"]),
    }


def _same_name_and_spec(teachers, person, spec):
    return list(teachers.find({"names": person, "specializations": spec}))


def _new_teacher(person):
    return {**person, "names": [person], "adt": None, "adts": [], "specializations": [],
            "rankings": [], "hires": [], "review": []}


def _add_adt(teacher, adt):
    if adt in teacher["adts"]:
        return
    teacher["adts"].append(adt)
    current = teacher["adt"]
    # A new-format ADT replaces an old one, never the other way round.
    if not current or NEW_ADT_PATTERN.match(adt) or not NEW_ADT_PATTERN.match(current):
        teacher["adt"] = adt


def _put(entries, entry, keys):
    """Replace the entry with the same keys, or append it."""
    for i, old in enumerate(entries):
        if all(old.get(k) == entry.get(k) for k in keys):
            entries[i] = entry
            return
    entries.append(entry)


def _lists(teacher):
    return {tuple(r.get(k) for k in RANKING_KEYS[:3]) for r in teacher["rankings"]}


def _add_name(teacher, person):
    teacher.update(person)
    if person not in teacher["names"]:
        teacher["names"].append(person)


def _merge(teachers, teacher, other):
    """Move everything from other into teacher and delete other."""
    for person in other["names"]:
        if person not in teacher["names"]:
            teacher["names"].append(person)
    for adt in other["adts"]:
        _add_adt(teacher, adt)
    for spec in other["specializations"]:
        if spec not in teacher["specializations"]:
            teacher["specializations"].append(spec)
    for r in other["rankings"]:
        _put(teacher["rankings"], r, RANKING_KEYS)
    for h in other["hires"]:
        _put(teacher["hires"], h, HIRE_KEYS)
    # other's review notes were about this ambiguity, which is now settled.
    teachers.delete_one({"_id": other["_id"]})


def _save(teachers, teacher):
    if "_id" in teacher:
        teachers.replace_one({"_id": teacher["_id"]}, teacher)
    else:
        teachers.insert_one(teacher)


RANKING_KEYS = ("pinakas_katataksis", "year_of_import", "specialization", "am")


def save_ranking(teachers, row, ranking):
    """Store one ranking list row.

    row:     {"lastname", "name", "father", "adt"} from the parser
    ranking: the parser's qualifications dict (needs the RANKING_KEYS)

    Match order:
    1. any ADT this teacher ever had;
    2. otherwise same full name + father + specialization, because the
       same teacher in the same specialization may come back with a new
       ADT. A candidate that already appears in this same list under a
       different application (am) is a namesake, not this person.
    Exactly one candidate is a match. Zero or several create a new
    teacher; several also leave a review note.
    """
    person = _person(row)
    adt = str(row["adt"]).strip() if valid_adt(row["adt"]) else None
    spec = ranking["specialization"]

    matches = list(teachers.find({"adts": adt})) if adt else []
    matched_by = "adt"
    same_name = _same_name_and_spec(teachers, person, spec)
    by_name = [
        t for t in same_name
        if not any(
            all(r.get(k) == ranking.get(k) for k in RANKING_KEYS[:3])
            and r.get("am") != ranking.get("am")
            for r in t["rankings"]
        )
    ]

    if not matches:
        matched_by = "name+spec"
        matches = by_name
    elif len(matches) == 1:
        # Found by ADT, but the same person may already exist under an
        # older ADT in this specialization: they first showed up with the
        # new ADT in another specialization (eg. ΠΕ01 before ΠΕ02).
        # Merge that record in, if there is exactly one.
        # Only when the two never appear in the same list (that would make
        # them two people) and nobody else could be that record too.
        others = [t for t in by_name if t["_id"] != matches[0]["_id"]]
        if len(others) == 1 and not (_lists(others[0]) & _lists(matches[0])):
            other = others[0]
            rivals = [
                t for t in same_name
                if t["_id"] not in (other["_id"], matches[0]["_id"])
                and not (_lists(t) & _lists(other))
            ]
            if not rivals:
                _merge(teachers, matches[0], other)

    if len(matches) == 1:
        teacher = matches[0]
        action = f"MATCHED ({matched_by})"
    else:
        teacher = _new_teacher(person)
        matched_by = "new"
        action = "CREATED"
        if matches:
            action = "CREATED (ambiguous)"
            teacher["review"].append({
                "reason": "several teachers with the same name and specialization",
                "candidates": [t["_id"] for t in matches],
                "file": ranking.get("file"),
            })

    _add_name(teacher, person)
    if adt:
        _add_adt(teacher, adt)
    if spec not in teacher["specializations"]:
        teacher["specializations"].append(spec)
    _put(teacher["rankings"], {**ranking, "adt": adt, "matched_by": matched_by}, RANKING_KEYS)

    _save(teachers, teacher)
    return teacher["_id"], action


HIRE_KEYS = ("school_year", "round", "specialization", "main_table_type")


def save_hire(teachers, hire):
    """Store one hire row (the parser's hire dict).

    Hire files have no ADT, so the match is same full name + father +
    specialization. If several teachers share it, the one whose ranking
    position (aa) equals the hire's ΣΕΙΡΑ ΠΙΝΑΚΑ breaks the tie.
    """
    hire = dict(hire)
    person = _person(hire)
    for k in ("lastname", "name", "father"):
        hire.pop(k)
    spec = hire["specialization"]

    matches = _same_name_and_spec(teachers, person, spec)
    already = [t for t in matches
               if any(all(h.get(k) == hire.get(k) for k in HIRE_KEYS) for h in t["hires"])]
    if len(already) == 1:
        # Re-importing a hire file: keep it on the teacher it went to.
        matches = already
    if len(matches) > 1:
        by_order = [
            t for t in matches
            if any(r.get("specialization") == spec and r.get("aa") == hire.get("main_table_order")
                   for r in t["rankings"])
        ]
        if len(by_order) == 1:
            matches = by_order

    if len(matches) == 1:
        teacher = matches[0]
        action = "MATCHED"
    else:
        teacher = _new_teacher(person)
        teacher["specializations"].append(spec)
        action = "CREATED"
        if matches:
            action = "CREATED (ambiguous)"
            teacher["review"].append({
                "reason": "hire matches several teachers with the same name and specialization",
                "candidates": [t["_id"] for t in matches],
                "school_year": hire.get("school_year"),
                "round": hire.get("round"),
            })

    _put(teacher["hires"], hire, HIRE_KEYS)

    _save(teachers, teacher)
    return teacher["_id"], action
