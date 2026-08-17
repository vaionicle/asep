from . import parse_int, parse_float

init_row = 1
end_row = 0


def cleanup(text):
    if text is None:
        return []

    return (
        str(text)
        .replace(" ", "-")
        .replace("---", "-")
        .replace("--", "-")
        .split("-")
    )


def hire(row, school_year, round):
    last_name = cleanup(row[3].value)
    name = cleanup(row[4].value)
    father = cleanup(row[5].value)

    return {
        "school_year": school_year,
        "round": round,

        "aa": parse_int(row[0].value),
        "aa_row": parse_int(row[1].value),

        # Used to find/join the educator.
        # These are NOT stored in the hires table.
        "lastname": last_name[0] if len(last_name) == 1 else last_name,
        "name": name[0] if len(name) == 1 else name,
        "father": father[0] if len(father) == 1 else father,

        "department": row[6].value,
        "specialization": row[7].value,

        "main_table_type": row[2].value,
        "main_table": row[8].value,
        "main_table_order": parse_int(row[9].value),
        "main_table_score": parse_float(row[10].value),

        "location": row[11].value,
        "working_hours": row[12].value,
        "management_sector": row[13].value,
        "state": row[14].value,
    }