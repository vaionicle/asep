from . import parse_int, parse_float

def ekpedeutikos(row):
    last_name   = row[2].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")
    name        = row[3].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")
    father      = row[4].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")

    try:
        adt = str(parse_int(row[5].value))
    except:
        adt = row[5].value

    adt = adt.replace(" ", "").replace("-", "")

    return {
        "name"          : name,
        "lastName"      : last_name,
        "father"        : father,
        "adt"           : adt if adt != "" else "N/A",
    }

def qualifications(row, fileName, spec):
    try:
        am = parse_int(row[1].value)
    except:
        am = 0

    return {
        "am": am,
        "file": fileName,
        "year_of_import": 2026,
        "specialization": spec,

        # Academic qualifications
        "vasikos_titlos_spoudon": parse_float(row[6].value),
        "deutero_ptyxio_aei":  parse_int(row[7].value),
        "didaktoriko_diploma": parse_int(row[8].value),
        "arithmos_autotelon_metaptyxiakon_titlon_i_integrated_masters": parse_int(row[9].value),
        "monades_metaptyxiakon_titlon_synolika": parse_int(row[10].value),

        # Foreign languages
        "aristi_gnosi_xenon_glosson": parse_int(row[11].value),
        "poly_kali_gnosi_xenon_glosson": parse_int(row[12].value),
        "kali_gnosi_xenon_glosson": parse_int(row[13].value),
        "synolo_monadon_xenon_glosson_eos_2": parse_int(row[14].value),

        # Computer skills
        "gnosi_xeirismou_iy": parse_int(row[15].value),

        # Academic training
        "epimorfosi_aei_toulaxiston_300_oron_7_minon": parse_int(row[16].value),
        "synolo_monadon_akadimaikon_prosonton": parse_float(row[17].value),

        # Teaching experience
        "mines_ekpaideutikis_proypiresias": row[18].value,
        "monades_ekpaideutikis_proypiresias": row[19].value,

        "mines_ekpaideutikis_proypiresias_se_dysprosita": row[20].value,
        "monades_ekpaideutikis_proypiresias_se_dysprosita": row[21].value,

        # 3-month contracts 2020-2021
        "mines_ekp_proyp_3minis_diarkeias_2020_2021": parse_float(row[22].value),
        "monades_ekp_proyp_3minis_diarkeias_2020_2021": parse_float(row[23].value),

        # 3-month contracts 2021-2022
        "mines_ekp_proyp_3minis_diarkeias_2021_2022": parse_float(row[24].value),
        "monades_ekp_proyp_3minis_diarkeias_2021_2022": parse_float(row[25].value),

        # 3-month contracts / hard-to-reach 2020-2021
        "mines_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021": parse_float(row[26].value),
        "monades_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021": parse_float(row[27].value),

        # 3-month contracts / hard-to-reach 2021-2022
        "mines_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022": parse_float(row[28].value),
        "monades_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022": parse_float(row[29].value),

        # Private education
        "mines_ekp_proyp_stin_idiotiki_ekpaideusi": row[30].value,
        "monades_ekp_proyp_stin_idiotiki_ekpaideusi": parse_float(row[31].value),

        # Digital tutoring
        "mines_ekp_proyp_sto_psifiako_frontistirio": parse_float(row[32].value),
        "monades_ekp_proyp_sto_psifiako_frontistirio": parse_float(row[33].value),

        # Total teaching experience
        "synolo_monadon_ekpaideutikis_proypiresias": parse_float(row[34].value),

        # Children
        "arithmos_teknon": row[35].value,
        "monades_teknon": row[36].value,

        # Disability
        "pososto_anapirias": parse_float(row[37].value),
        "monades_anapirias": parse_float(row[38].value),

        # Special qualifications
        "protaksi_logo_paidagogikis_didaktikis_eparkeias": True if row[39].value == "NAI" else False,

        # Ranking / lottery
        "seira_ilektronikis_klirosis_par_4_arthr_15_n_4765_2021": row[40].value,

        # Final score from CSV
        "total_score": parse_float(row[41].value),
    }

# [number:1.0, number:6224.0, text:'ΓΚΟΡΟΥ', text:'ΣΟΦΙΑ', text:'ΙΩΑΝΝΗΣ', text:'ΑΜ603570', number:18.33, number:0.0, number:40.0, number:20.0, number:14.0, empty:'', empty:'', number:14.0, number:4.0, number:2.0, number:98.33, number:120.0, number:120.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:120.0, number:6.0, number:0.0, text:'ΝΑΙ', number:224.33]
# Α/Α,Α.Μ. ΑΙΤΗΣΗΣ,ΕΠΩΝΥΜΟ,ΟΝΟΜΑ,ΠΑΤΡΩΝΥΜΟ,Α.Δ.Τ.,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,ΒΑΘΜΟΛΟΓΙΑ
# 1,80042,ΜΠΑΡΟΥΝΗ,ΜΑΡΙΑ,ΓΕΩΡΓΙΟΣ,ΑΖ508274,"22,6",0,40,2,28,7,,,7,4,0,"101,6",0,0,0,0,0,0,0,0,0,0,0,0,182,120,0,0,120,1,3,0,0,ΝΑΙ,2710028,"224,6"
# ----
# 1:ΒΑΣΙΚΟΣ ΤΙΤΛΟΣ ΣΠΟΥΔΩΝ
# 2:ΔΕΥΤΕΡΟ ΠΤΥΧΙΟ Α.Ε.Ι.
# 3:ΔΙΔΑΚΤΟΡΙΚΟ ΔΙΠΛΩΜΑ
# 4:ΑΡΙΘΜΟΣ ΑΥΤΟΤΕΛΩΝ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΤΙΤΛΩΝ Ή INTEGRATED MASTERS (ΕΩΣ 2)
# 5:ΜΟΝΑΔΕΣ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΤΙΤΛΩΝ ΣΥΝΟΛΙΚΑ
# 6:ΑΡΙΣΤΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
# 7:ΠΟΛΎ ΚΑΛΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
# 8:ΚΑΛΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
# 9:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΞΕΝΩΝ ΓΛΩΣΣΩΝ (ΕΩΣ 2)
# 10:ΓΝΩΣΗ ΧΕΙΡΙΣΜΟΥ Η/Υ
# 11:ΕΠΙΜΟΡΦΩΣΗ ΑΕΙ (ΤΟΥΛΑΧΙΣΤΟΝ 300 ΩΡΩΝ & 7 ΜΗΝΩΝ)
# 12:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΑΚΑΔΗΜΑΪΚΩΝ ΠΡΟΣΟΝΤΩΝ
# 13:ΜΗΝΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
# 14:ΜΟΝΑΔΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
# 15:ΜΗΝΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ ΣΕ ΔΥΣΠΡΟΣΙΤΑ
# 16:ΜΟΝΑΔΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ ΣΕ ΔΥΣΠΡΟΣΙΤΑ
# 17:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2020-2021
# 18:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2020-2021
# 19:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2021-2022
# 20:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2021-2022
# 21:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2020-2021
# 22:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2020-2021
# 23:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2021-2022
# 24:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2021-2022
# 25:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΗΝ ΙΔΙΩΤΙΚΗ ΕΚΠΑΙΔΕΥΣΗ
# 26:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΗΝ ΙΔΙΩΤΙΚΗ ΕΚΠΑΙΔΕΥΣΗ
# 27:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΟ ΨΗΦΙΑΚΟ ΦΡΟΝΤΙΣΤΗΡΙΟ
# 28:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΟ ΨΗΦΙΑΚΟ ΦΡΟΝΤΙΣΤΗΡΙΟ
# 29:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
# 30:ΑΡΙΘΜΟΣ ΤΕΚΝΩΝ
# 31:ΜΟΝΑΔΕΣ ΤΕΚΝΩΝ
# 32:ΠΟΣΟΣΤΟ ΑΝΑΠΗΡΙΑΣ
# 33:ΜΟΝΑΔΕΣ ΑΝΑΠΗΡΙΑΣ
# 34:ΠΡΟΤΑΞΗ ΛΟΓΩ ΠΑΙΔΑΓΩΓΙΚΗΣ/ΔΙΔΑΚΤΙΚΗΣ ΕΠΑΡΚΕΙΑΣ
# 35:ΣΕΙΡΑ ΗΛΕΚΤΡΟΝΙΚΗΣ ΚΛΗΡΩΣΗΣ (παρ.4. άρθρ.15, ν.4765/2021)

