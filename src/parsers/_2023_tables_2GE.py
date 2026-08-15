from . import parse_int, parse_float

init_row = 7
end_row = 29

def ekpedeutikos(row):
    last_name = row[2].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")
    name      = row[3].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")
    father    = row[4].value.replace(" ", "-").replace("---", "-").replace("--", "-").split("-")

    try:
        adt = str(parse_int(row[5].value))
    except:
        adt = row[5].value

    adt = adt.replace(" ", "").replace("-", "")

    return {
        "name": name.strip(),
        "lastName": last_name.strip(),
        "father": father.strip(),
        "adt": adt if adt != "" else "N/A",
    }


def qualifications(row, fileName, spec):
    try:
        am = parse_int(row[1].value)
    except:
        am = 0

    return {
        "aa": parse_int(row[0].value),
        "am": am,
        "file": fileName,
        "year_of_import": 2023,
        "specialization": spec,
        "pinakas_katataksis": "2GE",

        # --------------------------------------------------
        # Academic qualifications
        # --------------------------------------------------

        # 1: Βασικός Τίτλος
        "vasikos_titlos_spoudon": parse_float(row[6].value),

        # 2: Δεύτερο Πτυχίο Α.Ε.Ι
        "deutero_ptyxio_aei": parse_float(row[7].value),

        # 3: Διδακτορικό Δίπλωμα
        "didaktoriko_diploma": parse_float(row[8].value),

        # 4: Μεταπτυχιακός Τίτλος Σπουδών
        "monades_metaptyxiakon_titlon_synolika": parse_float(row[9].value),

        # --------------------------------------------------
        # Foreign languages
        # --------------------------------------------------

        # 5: Άριστη Γνώση Ξένης Γλώσσας
        "aristi_gnosi_xenon_glosson": parse_float(row[10].value),

        # 6: Πολύ Καλή Γνώση Ξένης Γλώσσας
        "poly_kali_gnosi_xenon_glosson": parse_float(row[11].value),

        # 7: Καλή Γνώση Ξένης Γλώσσας
        "kali_gnosi_xenon_glosson": parse_float(row[12].value),

        # 8: Συνολική Βαθμολογία Ξένων Γλωσσών
        "synolo_monadon_xenon_glosson_eos_2": parse_float(row[13].value),

        # --------------------------------------------------
        # Computer skills
        # --------------------------------------------------

        # 9: Γνώση Χειρισμού Η/Υ
        "gnosi_xeirismou_iy": parse_float(row[14].value),

        # --------------------------------------------------
        # Academic training
        # --------------------------------------------------

        # 10: Επιμόρφωση Διάρκειας 300 Ωρών
        "epimorfosi_aei_toulaxiston_300_oron_7_minon": parse_float(row[15].value),

        # 11: Συνολική Βαθμολογία Ακαδημαϊκών Προσόντων
        "synolo_monadon_akadimaikon_prosonton": parse_float(row[16].value),

        # --------------------------------------------------
        # Teaching experience
        # --------------------------------------------------

        # 12: Αριθμός Μηνών Εκπαιδευτικής Προϋπηρεσίας
        "mines_ekpaideutikis_proypiresias": parse_float(row[17].value),

        # 13: Βαθμολογία Εκπαιδευτικής Προϋπηρεσίας
        "monades_ekpaideutikis_proypiresias": parse_float(row[18].value),

        # 14: Αριθμός Μηνών σε Δυσπρόσιτες Σχολικές Μονάδες
        "mines_ekpaideutikis_proypiresias_se_dysprosita": parse_float(row[19].value),

        # 15: Βαθμολογία Μηνών σε Δυσπρόσιτες Σχολικές Μονάδες
        "monades_ekpaideutikis_proypiresias_se_dysprosita": parse_float(row[20].value),

        # --------------------------------------------------
        # 3-month contracts 2020-2021
        # --------------------------------------------------

        # 16
        "mines_ekp_proyp_3minis_diarkeias_2020_2021": parse_float(row[21].value),

        # 17
        "monades_ekp_proyp_3minis_diarkeias_2020_2021": parse_float(row[22].value),

        # --------------------------------------------------
        # 3-month contracts 2021-2022
        # --------------------------------------------------

        # 18
        "mines_ekp_proyp_3minis_diarkeias_2021_2022": parse_float(row[23].value),

        # 19
        "monades_ekp_proyp_3minis_diarkeias_2021_2022": parse_float(row[24].value),

        # --------------------------------------------------
        # 3-month hard-to-reach 2020-2021
        # --------------------------------------------------

        # 20
        "mines_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021": parse_float(row[25].value),

        # 21
        "monades_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021": parse_float(row[26].value),

        # --------------------------------------------------
        # 3-month hard-to-reach 2021-2022
        # --------------------------------------------------

        # 22
        "mines_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022": parse_float(row[27].value),

        # 23
        "monades_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022": parse_float(row[28].value),

        # --------------------------------------------------
        # Total teaching experience
        # --------------------------------------------------

        # 24: Συνολική Βαθμολογία Εκπαιδευτικής Προϋπηρεσίας
        "synolo_monadon_ekpaideutikis_proypiresias": parse_float(row[29].value),

        # --------------------------------------------------
        # Children
        # --------------------------------------------------

        # 25: Βαθμολογία Ανήλικων Τέκνων
        "monades_teknon": parse_float(row[30].value),

        # --------------------------------------------------
        # Disability
        # --------------------------------------------------

        # 26: Βαθμολογία Ποσοστού Αναπηρίας
        "monades_anapirias": parse_float(row[31].value),

        # --------------------------------------------------
        # Pedagogical qualification
        # --------------------------------------------------

        # 27: Παιδαγωγική Επάρκεια
        "protaksi_logo_paidagogikis_didaktikis_eparkeias": True if str(row[32].value).strip().upper() == "ΝΑΙ" else False,

        # --------------------------------------------------
        # Final score
        # --------------------------------------------------

        "total_score": parse_float(row[33].value),
    }

# 1:Βασικός Τίτλος
# 2:Δεύτερο Πτυχίο Α.Ε.Ι
# 3:Διδακτορικό Δίπλωμα
# 4:Μεταπτυχιακός Τίτλος Σπουδών

# 5:Άριστη Γνώση Ξένης Γλώσσας
# 6:Πολύ Καλή Γνώση Ξένης Γλώσσας
# 7:Καλή Γνώση Ξένης Γλώσσας
# 8:Συνολική Βαθμολογία Ξένων Γλωσσών

# 9:Γνώση Χειρισμού Η/Υ
# 10:Επιμόρφωση Διάρκειας 300 Ωρών
# 11:Συνολική Βαθμολογία Ακαδημαϊκών Προσόντων
# 12:Αριθμός Μηνών Εκπαιδευτικής Προϋπηρεσίας
# 13:Βαθμολογία Εκπαιδευτικής Προϋπηρεσίας

# 14:Αριθμός Μηνών Εκπ. Προϋπηρ. σε Δυσπρόσιτες Σχ.Μονάδες
# 15:Βαθμολογία Μηνών Εκπ. Προϋπηρ. σε Δυσπρόσιτες Σχ.Μονάδες

# 16:Αριθμός Μηνών Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2020-21
# 17:Βαθμολογία Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2020-21

# 18:Αριθμός Μηνών Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2021-22
# 19:Βαθμολογία Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2021-22

# 20:Αριθμός μηνών εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2020-21
# 21:Βαθμολογία εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2020-21

# 22:Αριθμός μηνών εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2021-22
# 23:Βαθμολογία εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2021-22

# 24:Συνολική Βαθμολογία Εκπαιδευτικής Προϋπηρεσίας
# 25:Βαθμολογία Ανήλικων Τέκνων
# 26:Βαθμολογία Ποσοστού Αναπηρίας
# 27:Παιδαγωγική Επάρκεια
