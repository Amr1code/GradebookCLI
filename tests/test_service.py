import unittest

from gradebook.service import (
    add_course,
    add_grade_to_enrollment,
    add_student,
    compute_student_average,
    enroll_student_in_course,
)


class TestService(unittest.TestCase):
    def setUp(self):
        self.data = {
            "students": [],
            "courses": [],
            "enrollments": [],
        }

    def test_add_student(self):
        created = add_student(self.data, "s1", "Dion")

        self.assertEqual(created["id"], "s1")
        self.assertEqual(created["name"], "Dion")
        self.assertEqual(len(self.data["students"]), 1)

        with self.assertRaises(ValueError):
            add_student(self.data, "s1", "Lorik")

    def test_add_grade(self):
        add_student(self.data, "s1", "Dion")
        add_course(self.data, "MAT101", "Mathematics")
        enroll_student_in_course(self.data, "s1", "MAT101")

        updated = add_grade_to_enrollment(self.data, "s1", "MAT101", 88)
        self.assertEqual(updated["grades"], [88.0])

        with self.assertRaises(ValueError):
            add_grade_to_enrollment(self.data, "s2", "MAT101", 75)

    def test_compute_average(self):
        add_student(self.data, "s1", "Arta")
        add_course(self.data, "CSC200", "Algorithms")
        enroll_student_in_course(self.data, "s1", "CSC200")

        add_grade_to_enrollment(self.data, "s1", "CSC200", 80)
        add_grade_to_enrollment(self.data, "s1", "CSC200", 90)

        average = compute_student_average(self.data, "s1")
        self.assertEqual(average, 85.0)

        no_grade_average = compute_student_average(self.data, "s2")
        self.assertIsNone(no_grade_average)


if __name__ == "__main__":
    unittest.main()