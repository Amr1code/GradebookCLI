"""Seed Gradebook CLI with mock Albanian data."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gradebook.storage import save_data


def build_seed_data():
    """Build mock gradebook data with students, courses, and enrollments.

    Returns:
        dict: Seed-ready gradebook data dictionary.
    """
    return {
        "students": [
            {"id": "s1", "name": "Arben"},
            {"id": "s2", "name": "Teuta"},
            {"id": "s3", "name": "Dritan"},
        ],
        "courses": [
            {"code": "MAT101", "title": "Matematikë"},
            {"code": "HIS201", "title": "Histori"},
            {"code": "LET301", "title": "Letërsi"},
        ],
        "enrollments": [
            {
                "student_id": "s1",
                "course_code": "MAT101",
                "grades": [88.0, 92.0],
            },
            {
                "student_id": "s1",
                "course_code": "HIS201",
                "grades": [81.0],
            },
            {
                "student_id": "s2",
                "course_code": "MAT101",
                "grades": [95.0, 90.0],
            },
            {
                "student_id": "s2",
                "course_code": "LET301",
                "grades": [87.0],
            },
            {
                "student_id": "s3",
                "course_code": "HIS201",
                "grades": [78.0, 84.0],
            },
        ],
    }


def main():
    """Generate and persist seed data to the default JSON store."""
    seed_data = build_seed_data()
    save_data(seed_data, "data/gradebook.json")
    print("Seed data created successfully at data/gradebook.json")


if __name__ == "__main__":
    main()