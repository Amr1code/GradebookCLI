def parse_non_empty(value, field_name):
    if value is None:
        raise ValueError(f"{field_name} is required")

    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")

    return cleaned


def parse_grade(grade_str):
    try:
        grade = float(str(grade_str).strip())
    except (TypeError, ValueError):
        raise ValueError("Grade must be a valid number between 0 and 100")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade