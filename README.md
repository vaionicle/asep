# asep

Extract data from Greek ASEP for education

## Database Schema

```mysql
| Ekpedeutikoi |
| ------------ |
| id           |
| AM           |
| name         |
| last_name    |
| fathers_name |
| adt          |

| qualifications                                                         |
| ---------------------------------------------------------------------- |
| id                                                                     |
| ekpedeutikos_id                                                        |
| 01.vasikos_titlos                                                      |
| 02.deutero_ptyxeio_aei                                                 |
| 03.didaktoriko_diploma                                                 |
| 04.metaptixiako                                                        |
| 05.aristi_gnosi_ksenis_glossas                                         |
| 06.poli_kali_gnosi_ksenis_glossas                                      |
| 07.kali_gnosi_ksenis_glossas                                           |
| 08.sunoliki_vathmologia_ksenis_glossas                                 |
| 09.gnosi_yh                                                            |
| 10.epimorfosi_300_ores                                                 |
| 11.sunoloki_vathmologia_akadimaikon_prosonton                          |
| 12.arithmos_minon_ekpedeusis                                           |
| 13.vathmologia_ekpaideutikis_prouphresias                              |
| 14.Αριθμός Μηνών Εκπ. Προϋπηρ. σε Δυσπρόσιτες Σχ.Μονάδες               |
| 15.Βαθμολογία Μηνών Εκπ. Προϋπηρ. σε Δυσπρόσιτες Σχ.Μονάδες            |
| 16.Αριθμός Μηνών Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2020-21 |
| 17.Βαθμολογία Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2020-21    |
| 18.Αριθμός Μηνών Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2021-22 |
| 19.Βαθμολογία Εκπ. Προϋπηρ. 3μηνης διάρκειας σχολικού έτους 2021-22    |
| 20.Αριθμός μηνών εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2020-21    |
| 21.Βαθμολογία εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2020-21       |
| 22.Αριθμός μηνών εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2021-22    |
| 23.Βαθμολογία εκπ. προϋπ. 3μηνης διάρκειας σε δυσπρόσιτα 2021-22       |
| 24.Συνολική Βαθμολογία Εκπαιδευτικής Προϋπηρεσίας                      |
| 25.Βαθμολογία Ανήλικων Τέκνων                                          |
| 26.Βαθμολογία Ποσοστού Αναπηρίας                                       |
| 27.Παιδαγωγική Επάρκεια                                                |

```


google

πινακεσ αναπληρωτων προσληψεις site:www.minedu.gov.gr