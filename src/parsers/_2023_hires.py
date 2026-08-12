from . import parse_int

def cleanup(text):
    return text.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")

def hire(row, school_year, round):

    last_name   = cleanup(row[3].value)
    name        = cleanup(row[4].value)
    father      = cleanup(row[5].value)

    return {
        "round"             : round,
        "school_year"       : school_year,

        "a/a"               : parse_int(row[0].value),
        "a/a_row"           : parse_int(row[1].value),

        "lastname"          : last_name[0]  if len(last_name) == 1 else last_name,
        "name"              : name[0]       if len(name) == 1 else name,
        "father"            : father[0]     if len(father) == 1 else father,

        "department"        : row[6].value,
        "spec"              : row[7].value,

        "main_table_type"   : row[2].value,
        "main_table"        : row[8].value,
        "main_table_order"  : parse_int(row[9].value),
        "main_table_score"  : row[10].value,

        "working_hours"     : row[12].value,
        "location"          : row[11].value,
        "management_sector" : row[13].value,
        "state"             : row[14].value,
    }

# [
    # 0 number:4909.0
    # 1 number:193.0

    # 2 text:'ΓΕΝΙΚΗΣ ΠΑΙΔΕΙΑΣ'

    # 3 text:'ΣΤΡΑΤΗΓΑΚΗ'
    # 4 text:'ΑΙΚΑΤΕΡΙΝΗ'
    # 5 text:'ΑΘΑΝΑΣΙΟΣ'

    # 6 text:'ΠΕ91.01'
    # 7 text:'ΠΕ91.01'
    # 8 text:'Α'
    # 9 number:212.0
    # 10 number:141.33

    # 11 text:'ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑΣ (Δ.Ε.)'
    # 12 text:'ΑΠΩ'
    # 13 text:'ΔΙΕΥΘΥΝΣΗ Δ.Ε. ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑΣ'
    # 14 text:'ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ'
# ]