import json
import os


def _empty_data():
    return {
        "students": [],
        "courses": [],
        "enrollments": [],
    }


def load_data(filepath="data/gradebook.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print(f"Warning: Invalid data format in '{filepath}'. Using empty data.")
            return _empty_data()

        data.setdefault("students", [])
        data.setdefault("courses", [])
        data.setdefault("enrollments", [])
        return data

    except FileNotFoundError:
        return _empty_data()
    except json.JSONDecodeError:
        print(f"Error: The file '{filepath}' is corrupted or not valid JSON.")
        return _empty_data()
    except OSError as exc:
        print(f"Error reading '{filepath}': {exc}")
        return _empty_data()


def save_data(data, filepath="data/gradebook.json"):
    try:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except OSError as exc:
        print(f"Error saving data to '{filepath}': {exc}")