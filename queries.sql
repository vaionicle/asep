SELECT *
FROM educator as e
INNER JOIN qualifications as q
WHERE e.id = q.educator_id
AND e.adt = "ΑΜ327077"
GROUP BY e.adt
HAVING count(*) > 1



SELECT 
    q.aa,
    q.am,
    e.lastname,
    e.name,
    e.father,
    e.adt,
    -- q.vasikos_titlos_spoudon as "01",
    -- q.deutero_ptyxio_aei as "02",
    -- q.didaktoriko_diploma as "03",
    -- q.arithmos_autotelon_metaptyxiakon_titlon_i_integrated_masters as "04",
    -- q.monades_metaptyxiakon_titlon_synolika as "05",
    -- q.aristi_gnosi_xenon_glosson as "06",
    -- q.poly_kali_gnosi_xenon_glosson as "07",
    -- q.kali_gnosi_xenon_glosson as "08",
    -- q.synolo_monadon_xenon_glosson_eos_2 as "09",
    -- q.gnosi_xeirismou_iy as "10",
    -- q.epimorfosi_aei_toulaxiston_300_oron_7_minon as "11",
    q.synolo_monadon_akadimaikon_prosonton as "12",
    q.mines_ekpaideutikis_proypiresias / 12 as "13",
    -- q.monades_ekpaideutikis_proypiresias as "14",
    q.mines_ekpaideutikis_proypiresias_se_dysprosita / 12 as "15",
    -- q.monades_ekpaideutikis_proypiresias_se_dysprosita as "16",
    -- q.mines_ekp_proyp_3minis_diarkeias_2020_2021 as "17",
    -- q.monades_ekp_proyp_3minis_diarkeias_2020_2021 as "18",
    -- q.mines_ekp_proyp_3minis_diarkeias_2021_2022 as "19",
    -- q.monades_ekp_proyp_3minis_diarkeias_2021_2022 as "20",
    -- q.mines_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021 as "21",
    -- q.monades_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021 as "22",
    -- q.mines_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022 as "23",
    -- q.monades_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022 as "24",
    q.mines_ekp_proyp_stin_idiotiki_ekpaideusi / 12  as "25",
    -- q.monades_ekp_proyp_stin_idiotiki_ekpaideusi as "26",
    q.mines_ekp_proyp_sto_psifiako_frontistirio / 12 as "27",
    -- q.monades_ekp_proyp_sto_psifiako_frontistirio as "28",
    -- q.synolo_monadon_ekpaideutikis_proypiresias as "29",
    -- q.arithmos_teknon as "30",
    -- q.monades_teknon as "31",
    q.pososto_anapirias as "32",
    -- q.monades_anapirias as "33",
    -- q.protaksi_logo_paidagogikis_didaktikis_eparkeias as "34",
    -- q.seira_ilektronikis_klirosis_par_4_arthr_15_n_4765_2021 as "35",
    q.total_score as "score"
FROM educator as e
INNER JOIN qualifications as q
WHERE
    e.id = q.educator_id
    AND q.specialization = "ΠΕ02"
    AND q.aa <= 1333
    -- AND q.pososto_anapirias > 80
    -- AND q.mines_ekp_proyp_stin_idiotiki_ekpaideusi > 0
    -- AND q.mines_ekpaideutikis_proypiresias > 0
;


SELECT 
    q.aa,
    q.am,
    e.lastname,
    e.name,
    e.father,
    e.adt,
    q.synolo_monadon_akadimaikon_prosonton as "12",
    q.mines_ekpaideutikis_proypiresias / 12 as "13",
    q.mines_ekpaideutikis_proypiresias_se_dysprosita / 12 as "15",
    q.mines_ekp_proyp_stin_idiotiki_ekpaideusi / 12  as "25",
    q.mines_ekp_proyp_sto_psifiako_frontistirio / 12 as "27",
    q.pososto_anapirias as "32",
    q.total_score as "score"
FROM educator as e
INNER JOIN qualifications as q
WHERE
    e.id = q.educator_id
    AND q.specialization = "ΠΕ02"
    AND q.aa <= 1333
;

-- 5:ΜΟΝΑΔΕΣ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΤΙΤΛΩΝ ΣΥΝΟΛΙΚΑ
-- 6:ΑΡΙΣΤΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
-- 7:ΠΟΛΎ ΚΑΛΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
-- 8:ΚΑΛΗ ΓΝΩΣΗ ΞΕΝΩΝ ΓΛΩΣΣΩΝ
-- 9:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΞΕΝΩΝ ΓΛΩΣΣΩΝ (ΕΩΣ 2)
-- 10:ΓΝΩΣΗ ΧΕΙΡΙΣΜΟΥ Η/Υ
-- 11:ΕΠΙΜΟΡΦΩΣΗ ΑΕΙ (ΤΟΥΛΑΧΙΣΤΟΝ 300 ΩΡΩΝ & 7 ΜΗΝΩΝ)
-- 12:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΑΚΑΔΗΜΑΪΚΩΝ ΠΡΟΣΟΝΤΩΝ
-- 13:ΜΗΝΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
-- 14:ΜΟΝΑΔΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
-- 15:ΜΗΝΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ ΣΕ ΔΥΣΠΡΟΣΙΤΑ
-- 16:ΜΟΝΑΔΕΣ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ ΣΕ ΔΥΣΠΡΟΣΙΤΑ
-- 17:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2020-2021
-- 18:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2020-2021
-- 19:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2021-2022
-- 20:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ 2021-2022
-- 21:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2020-2021
-- 22:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2020-2021
-- 23:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2021-2022
-- 24:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. 3ΜΗΝΗΣ ΔΙΑΡΚΕΙΑΣ-ΔΥΣΠΡΟΣΙΤΑ 2021-2022
-- 25:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΗΝ ΙΔΙΩΤΙΚΗ ΕΚΠΑΙΔΕΥΣΗ
-- 26:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΗΝ ΙΔΙΩΤΙΚΗ ΕΚΠΑΙΔΕΥΣΗ
-- 27:ΜΗΝΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΟ ΨΗΦΙΑΚΟ ΦΡΟΝΤΙΣΤΗΡΙΟ
-- 28:ΜΟΝΑΔΕΣ ΕΚΠ. ΠΡΟΫΠ. ΣΤΟ ΨΗΦΙΑΚΟ ΦΡΟΝΤΙΣΤΗΡΙΟ
-- 29:ΣΥΝΟΛΟ ΜΟΝΑΔΩΝ ΕΚΠΑΙΔΕΥΤΙΚΗΣ ΠΡΟΫΠΗΡΕΣΙΑΣ
-- 30:ΑΡΙΘΜΟΣ ΤΕΚΝΩΝ
-- 31:ΜΟΝΑΔΕΣ ΤΕΚΝΩΝ
-- 32:ΠΟΣΟΣΤΟ ΑΝΑΠΗΡΙΑΣ
-- 33:ΜΟΝΑΔΕΣ ΑΝΑΠΗΡΙΑΣ
-- 34:ΠΡΟΤΑΞΗ ΛΟΓΩ ΠΑΙΔΑΓΩΓΙΚΗΣ/ΔΙΔΑΚΤΙΚΗΣ ΕΠΑΡΚΕΙΑΣ
-- 35:ΣΕΙΡΑ ΗΛΕΚΤΡΟΝΙΚΗΣ ΚΛΗΡΩΣΗΣ (παρ.4. άρθρ.15, ν.4765/2021)



-- FIND DUPLICATE POSITIONS
select qq.specialization, ee.*, qq.* 
from educator as ee 
inner join qualifications as qq
where ee.id in (
    SELECT e.id
    FROM educator as e
    INNER JOIN qualifications as q
    WHERE e.id = q.educator_id
    GROUP BY e.adt
    HAVING count(*) > 1
) 
AND ee.id = qq.educator_id
AND ee.adt = "ΑΜ327077"
Order By ee.adt;

select * from educator;



select q.specialization, e.*, q.*
from educator as e 
inner join qualifications as q
where
    e.id = q.educator_id
    AND lastname = "ΚΑΡΑΚΩΣΤΑ" ;

-- TRUNCATE TABLES
truncate table educator;
truncate table qualifications;