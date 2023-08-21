def ekpedeutikos(row, fileName):
    # a1 = sheet.cell_value(rowx=0, colx=0)

    # print(type(row[1].value))
    # print(type(row[1].cell_value()))
    
    return {
        "am": row[1].value,
        "name": row[3].value,
        "lastname": row[2].value,
        "father": row[4].value,
        "adt": row[5].value
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

def qualifications(row, fileName):
    return {
        "file": fileName,

        "am": row[1].value,
        "01.first_degree": row[6].value,
        "02.second_degree": row[7].value,
        "03.doctor_degree": row[8].value,
        "04.master_degree": row[9].value,

        "05.perfect_knowledge_foreign_language": row[10].value,
        "06.very_good_knowledge_foreign_language": row[11].value,
        "07.good_knowledge_foreign_language": row[12].value,
        "08.foreign_language_score": row[13].value,

        "09.computers": row[14].value,
        "10.300_hours": row[15].value,
        "11.total_score_of_academic": row[16].value,
        "12.month_of_education_experience": row[17].value,
        "13.score_of_education_experience": row[18].value,

        "14.number_of_months_hard_to_reach_schools": row[19].value,
        "15.score_hard_to_reach_schools": row[20].value,

        "16.": row[21].value,
        "17.": row[22].value,
        "18.": row[23].value,
        "19.": row[24].value,
        "20.": row[25].value,
        "21.": row[26].value,
        "22.": row[27].value,
        "23.": row[28].value,

        "24.working_experience": row[29].value,
        "25.kids": row[30].value,
        "26.amea": row[31].value,
        "27.paidagogiki_eparkeia": row[32].value,

        "total_score": row[33].value,
    }

# [number:1.0, number:6224.0, text:'ΓΚΟΡΟΥ', text:'ΣΟΦΙΑ', text:'ΙΩΑΝΝΗΣ', text:'ΑΜ603570', number:18.33, number:0.0, number:40.0, number:20.0, number:14.0, empty:'', empty:'', number:14.0, number:4.0, number:2.0, number:98.33, number:120.0, number:120.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:0.0, number:120.0, number:6.0, number:0.0, text:'ΝΑΙ', number:224.33]
