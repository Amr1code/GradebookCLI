import json
import logging
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
        logging.info("Data loaded successfully from '%s'", filepath)
        return data

    except FileNotFoundError:
        logging.error("Data file not found: '%s'", filepath, exc_info=True)
        return _empty_data()
    except json.JSONDecodeError:
        logging.error("JSON decode failed for '%s'", filepath, exc_info=True)
        print(f"Error: The file '{filepath}' is corrupted or not valid JSON.")
        return _empty_data()
    except OSError as exc:
        logging.error("OS error while reading '%s'", filepath, exc_info=True)
        print(f"Error reading '{filepath}': {exc}")
        return _empty_data()


def save_data(data, filepath="data/gradebook.json"):
    try:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        logging.info("Data saved successfully to '%s'", filepath)
    except OSError as exc:
        logging.error("OS error while saving '%s'", filepath, exc_info=True)
        print(f"Error saving data to '{filepath}': {exc}")