# CLAUDE.md

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
---

# Project: asep (Minedu educators)

## What this is

Imports Greek public school teacher data into MongoDB, one document per teacher.

- **Ranking lists (πίνακες κατάταξης)** from ASEP: `tmp/pinakes/`. Each row is one application (`am`) of one teacher in one specialization, with personal details (last name, name, father's name, ID/ADT) and all qualification scores. Lists are reissued every few years: 2ΓΕ 2019, 2023, 2026 (general education), 2ΕΑ 2025 (special education). Links are in README.md.
- **Hire files (προσλήψεις αναπληρωτών)** from minedu.gov.gr: `tmp/anaplirotes/<school year>/<phase>_fasi/`. Minedu hires temporary teachers in phases: the first each September, then roughly one a month. Each phase publishes excels per level (ΠΕ = primary, ΔΕ = secondary, ΕΑΕ = special education, Μουσικά = music schools) saying who is hired and where. They have no ADT, only name, father's name and specialization.
- **Permanent appointments (διορισμοί)**: `tmp/diorismoi/`. Not imported yet.

## Identity rules (the hard part)

All matching lives in `src/store.py`; the tests in `tests/test_store.py` use real names from the lists.

- The same teacher in the same specialization may come back in a newer list with a **new ADT** (eg. old `ΑΚ937853` → new `Α03300568`, one Greek letter + 8 digits). Never create a duplicate for that: match on full name + father's name + specialization and keep every ADT seen in `adts`. The new-format ADT becomes `adt`.
- A teacher can be in **several specializations**; that is one teacher with several rankings.
- Names are compared after `store.normalize` (upper case, accents removed, spaces collapsed). Never match on name prefixes: ΓΕΩΡΓΙΟΣ/ΙΩΑΝΝΗΣ and ΓΕΩΡΓΙΑ/ΙΩΑΝΝΑ are two people.
- Two rows with the same name in the **same list** but different `am` are two people (real namesakes exist).
- When a match is ambiguous, create a new teacher and add a note to its `review` list. Never guess.
- Hires match on name + father + specialization; if several teachers share it, the ranking position (`aa`) equal to the hire's ΣΕΙΡΑ ΠΙΝΑΚΑ breaks the tie.
- Re-running an import must not change anything. Import rankings before hires.

## Teacher document

```
{ lastname, name, father, adt, adts: [...], specializations: [...],
  rankings: [ {pinakas_katataksis, year_of_import, specialization, am, aa, total_score, ...all scores, adt, matched_by} ],
  hires:    [ {school_year, round, specialization, main_table_type, main_table, main_table_order, location, ...} ],
  review:   [ {reason, candidates, ...} ] }
```

## Layout and commands

- `src/parsers/` one module per file layout (`_2023_tables_2GE`, `_2026_tables_2GE`, `_2025_tables_2EA`, `_2023_hires`, `_2025_hires`). Parsers only turn an xls row into a dict; they never touch the database.
- `src/import_qualifications.py SPEC FILE YEAR`, `src/import_hires.py LAYOUT SCHOOL_YEAR ROUND FILE`. Paths are relative to `tmp/`; scripts run inside Docker at `/opt/asep`.
- `scripts/2ge_2023.sh`, `scripts/2ge_2026.sh`, `scripts/hires_de.sh` print one `make` command per file; `./run.sh` (`make import.all`) runs them all.
- `make build`, `make db.run` (Mongo on `mongo:27017`, override with `MONGO_URL`), `make test` (or `python -m unittest discover -s tests` locally; needs `mongomock`).
- Convert `.xlsx` to `.xls` with `make convert` before parsing (xlrd reads only `.xls`).

## Milestones

1. All secondary (high school) teachers in Mongo with no issues and no duplicates. ← current
2. A site with statistics from the temporary hires.
3. Permanent hires (διορισμοί) in the database.

Later: all school levels (kindergarten and primary need their ranking lists added), and the 2ΕΑ 2025 lists (parser exists but is not wired in yet).
