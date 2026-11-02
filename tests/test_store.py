import os
import sys
import unittest

import mongomock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import store  # noqa: E402


def ranking(year, spec, am, aa=1):
    return {"pinakas_katataksis": "2GE", "year_of_import": year,
            "specialization": spec, "am": am, "aa": aa, "total_score": 100.0}


def person(lastname, name, father, adt):
    return {"lastname": [lastname], "name": [name], "father": [father], "adt": adt}


class StoreTest(unittest.TestCase):
    # Names and IDs below are real cases from the 2ΓΕ 2023 and 2026 lists.

    def setUp(self):
        self.teachers = store.get_teachers(mongomock.MongoClient())

    def test_new_adt_in_same_specialization_is_the_same_teacher(self):
        store.save_ranking(self.teachers, person("ΜΑΛΑΜΑΤΑΡΗΣ", "ΔΗΜΗΤΡΙΟΣ", "ΑΛΚΙΒΙΑΔΗΣ", "ΑΚ937853"), ranking(2023, "ΠΕ81", 10))
        _, action = store.save_ranking(self.teachers, person("ΜΑΛΑΜΑΤΑΡΗΣ", "ΔΗΜΗΤΡΙΟΣ", "ΑΛΚΙΒΙΑΔΗΣ", "Α03300568"), ranking(2026, "ΠΕ81", 20))

        self.assertEqual(action, "MATCHED (name+spec)")
        self.assertEqual(self.teachers.count_documents({}), 1)
        teacher = self.teachers.find_one()
        self.assertEqual(teacher["adt"], "Α03300568")
        self.assertEqual(teacher["adts"], ["ΑΚ937853", "Α03300568"])
        self.assertEqual(len(teacher["rankings"]), 2)

    def test_reimporting_the_older_list_after_the_id_change(self):
        store.save_ranking(self.teachers, person("ΜΑΛΑΜΑΤΑΡΗΣ", "ΔΗΜΗΤΡΙΟΣ", "ΑΛΚΙΒΙΑΔΗΣ", "ΑΚ937853"), ranking(2023, "ΠΕ81", 10))
        store.save_ranking(self.teachers, person("ΜΑΛΑΜΑΤΑΡΗΣ", "ΔΗΜΗΤΡΙΟΣ", "ΑΛΚΙΒΙΑΔΗΣ", "Α03300568"), ranking(2026, "ΠΕ81", 20))
        _, action = store.save_ranking(self.teachers, person("ΜΑΛΑΜΑΤΑΡΗΣ", "ΔΗΜΗΤΡΙΟΣ", "ΑΛΚΙΒΙΑΔΗΣ", "ΑΚ937853"), ranking(2023, "ΠΕ81", 10))

        self.assertEqual(action, "MATCHED (adt)")
        teacher = self.teachers.find_one()
        self.assertEqual(self.teachers.count_documents({}), 1)
        self.assertEqual(teacher["adt"], "Α03300568")
        self.assertEqual(len(teacher["rankings"]), 2)

    def test_same_adt_in_two_specializations_is_one_teacher(self):
        store.save_ranking(self.teachers, person("ΓΚΟΡΟΥ", "ΣΟΦΙΑ", "ΙΩΑΝΝΗΣ", "ΑΜ603570"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΓΚΟΡΟΥ", "ΣΟΦΙΑ", "ΙΩΑΝΝΗΣ", "ΑΜ603570"), ranking(2023, "ΠΕ06", 2))

        teacher = self.teachers.find_one()
        self.assertEqual(self.teachers.count_documents({}), 1)
        self.assertEqual(teacher["specializations"], ["ΠΕ02", "ΠΕ06"])

    def test_accents_and_spelling_of_the_same_adt(self):
        store.save_ranking(self.teachers, person("ΠΟΥΤΙΔΟΥ", "ΆΝΝΑ", "ΧΡΗΣΤΟΣ", "ΑΜ430858"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΠΟΥΤΙΔΟΥ", "ΑΝΝΑ", "ΧΡΗΣΤΟΣ", "ΑΜ430858"), ranking(2026, "ΠΕ02", 2))

        self.assertEqual(self.teachers.count_documents({}), 1)
        self.assertEqual(self.teachers.find_one()["name"], "ΑΝΝΑ")

    def test_hire_matches_an_older_spelling_of_the_name(self):
        store.save_ranking(self.teachers, person("ΡΟΥΣΣΟΥ", "ΝΙΚΟΛΕΤΤΑ", "ΕΛΕΥΘΕΡΙΟΣ", "ΑΜ355899"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΡΟΥΣΣΟΥ", "ΝΙΚΟΛΕΤΑ", "ΕΛΕΥΘΕΡΙΟΣ", "ΑΜ355899"), ranking(2026, "ΠΕ02", 2))
        _, action = store.save_hire(self.teachers, {"lastname": "ΡΟΥΣΣΟΥ", "name": "ΝΙΚΟΛΕΤΤΑ", "father": "ΕΛΕΥΘΕΡΙΟΣ",
                                                    "specialization": "ΠΕ02", "school_year": "2023-24", "round": "C"})

        self.assertEqual(action, "MATCHED")
        self.assertEqual(self.teachers.count_documents({}), 1)
        self.assertEqual(self.teachers.find_one()["name"], "ΝΙΚΟΛΕΤΑ")

    def test_new_adt_in_another_specialization_is_not_merged_by_name(self):
        store.save_ranking(self.teachers, person("ΚΟΚΚΙΝΗ", "ΑΠΟΣΤΟΛΙΑ", "ΙΩΑΝΝΗΣ", "ΑΕ713182"), ranking(2023, "ΠΕ81", 1))
        store.save_ranking(self.teachers, person("ΚΟΚΚΙΝΗ", "ΑΠΟΣΤΟΛΙΑ", "ΙΩΑΝΝΗΣ", "Α00409521"), ranking(2026, "ΠΕ02", 2))

        self.assertEqual(self.teachers.count_documents({}), 2)

    def test_similar_names_are_not_merged(self):
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΣ", "ΓΕΩΡΓΙΟΣ", "ΙΩΑΝΝΗΣ", "ΑΒ111111"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΣ", "ΓΕΩΡΓΙΑ", "ΙΩΑΝΝΑ", "Α00000001"), ranking(2026, "ΠΕ02", 2))

        self.assertEqual(self.teachers.count_documents({}), 2)

    def test_namesakes_in_the_same_list_are_two_teachers(self):
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "Α00000001"), ranking(2026, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "Α00000002"), ranking(2026, "ΠΕ02", 2))

        self.assertEqual(self.teachers.count_documents({}), 2)

    def test_namesakes_changing_id_together_are_flagged_not_merged(self):
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000001"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000002"), ranking(2023, "ΠΕ02", 2))
        _, action = store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "Α00000001"), ranking(2026, "ΠΕ02", 3))

        self.assertEqual(action, "CREATED (ambiguous)")
        self.assertEqual(self.teachers.count_documents({"review.0": {"$exists": True}}), 1)

    def test_new_adt_first_seen_in_another_specialization(self):
        # 2023: ΠΕ02 with the old ADT. 2026: ΠΕ01 first, then ΠΕ02, both with the new ADT.
        store.save_ranking(self.teachers, person("ΜΠΑΜΠΑΤΖΑΝΗΣ", "ΣΩΤΗΡΙΟΣ", "ΣΤΥΛΙΑΝΟΣ", "ΑΗ150675"), ranking(2023, "ΠΕ02", 40357))
        store.save_ranking(self.teachers, person("ΜΠΑΜΠΑΤΖΑΝΗΣ", "ΣΩΤΗΡΙΟΣ", "ΣΤΥΛΙΑΝΟΣ", "Α03039065"), ranking(2026, "ΠΕ01", 68041))
        store.save_ranking(self.teachers, person("ΜΠΑΜΠΑΤΖΑΝΗΣ", "ΣΩΤΗΡΙΟΣ", "ΣΤΥΛΙΑΝΟΣ", "Α03039065"), ranking(2026, "ΠΕ02", 68041))

        self.assertEqual(self.teachers.count_documents({}), 1)
        teacher = self.teachers.find_one()
        self.assertEqual(teacher["adt"], "Α03039065")
        self.assertEqual(sorted(teacher["adts"]), sorted(["ΑΗ150675", "Α03039065"]))
        self.assertEqual(len(teacher["rankings"]), 3)

    def test_two_people_with_one_name_in_the_newer_list_stay_apart_on_reimport(self):
        # 2023 has one ΠΑΠΑΓΙΑΝΝΗ ΑΝΝΑ ΙΩΑΝΝΗΣ in ΠΕ02, 2026 has two.
        rows = [("ΑΖ834938", 2023, 39470), ("ΑΖ834938", 2026, 1020), ("ΑΝ378801", 2026, 79639)]
        for _ in range(2):
            for adt, year, am in rows:
                store.save_ranking(self.teachers, person("ΠΑΠΑΓΙΑΝΝΗ", "ΑΝΝΑ", "ΙΩΑΝΝΗΣ", adt), ranking(year, "ΠΕ02", am))

        self.assertEqual(self.teachers.count_documents({}), 2)
        self.assertEqual(self.teachers.count_documents({"adts": "ΑΝ378801"}), 1)
        self.assertEqual(len(self.teachers.find_one({"adts": "ΑΝ378801"})["rankings"]), 1)

    def test_reimporting_a_file_changes_nothing(self):
        for _ in range(2):
            store.save_ranking(self.teachers, person("ΓΚΟΡΟΥ", "ΣΟΦΙΑ", "ΙΩΑΝΝΗΣ", "ΑΜ603570"), ranking(2023, "ΠΕ02", 1))
            store.save_hire(self.teachers, {"lastname": "ΓΚΟΡΟΥ", "name": "ΣΟΦΙΑ", "father": "ΙΩΑΝΝΗΣ",
                                            "specialization": "ΠΕ02", "school_year": "2023-24", "round": "A"})

        teacher = self.teachers.find_one()
        self.assertEqual(self.teachers.count_documents({}), 1)
        self.assertEqual(len(teacher["rankings"]), 1)
        self.assertEqual(len(teacher["hires"]), 1)

    def test_reimporting_an_ambiguous_hire_does_not_add_teachers(self):
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000001"), ranking(2023, "ΠΕ02", 1, aa=10))
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000002"), ranking(2023, "ΠΕ02", 2, aa=20))
        hire = {"lastname": "ΠΑΠΑΔΟΠΟΥΛΟΥ", "name": "ΜΑΡΙΑ", "father": "ΓΕΩΡΓΙΟΣ",
                "specialization": "ΠΕ02", "school_year": "2023-24", "round": "A", "main_table_order": 99}

        _, first = store.save_hire(self.teachers, hire)
        _, second = store.save_hire(self.teachers, hire)

        self.assertEqual(first, "CREATED (ambiguous)")
        self.assertEqual(second, "MATCHED")
        self.assertEqual(self.teachers.count_documents({}), 3)

    def test_hire_tie_broken_by_ranking_order(self):
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000001"), ranking(2023, "ΠΕ02", 1, aa=10))
        store.save_ranking(self.teachers, person("ΠΑΠΑΔΟΠΟΥΛΟΥ", "ΜΑΡΙΑ", "ΓΕΩΡΓΙΟΣ", "ΑΒ000002"), ranking(2023, "ΠΕ02", 2, aa=20))
        _, action = store.save_hire(self.teachers, {"lastname": ["ΠΑΠΑΔΟΠΟΥΛΟΥ"], "name": "ΜΑΡΙΑ", "father": "ΓΕΩΡΓΙΟΣ",
                                                    "specialization": "ΠΕ02", "school_year": "2023-24", "round": "A",
                                                    "main_table_order": 20})

        self.assertEqual(action, "MATCHED")
        self.assertEqual(self.teachers.find_one({"adt": "ΑΒ000002"})["hires"][0]["round"], "A")

    def test_missing_adt_is_not_used_for_matching(self):
        store.save_ranking(self.teachers, person("Α", "Β", "Γ", "0"), ranking(2023, "ΠΕ02", 1))
        store.save_ranking(self.teachers, person("Δ", "Ε", "Ζ", "0"), ranking(2023, "ΠΕ02", 2))

        self.assertEqual(self.teachers.count_documents({}), 2)


if __name__ == "__main__":
    unittest.main()
