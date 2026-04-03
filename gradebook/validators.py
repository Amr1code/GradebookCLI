def parse_non_empty(value, field_name):
    """Normalize and validate non-empty CLI text input.

    Args:
        value (object): Raw input value.
        field_name (str): Field label for error messages.

    Returns:
        str: Trimmed non-empty string value.

    Raises:
        ValueError: If the input is missing or empty after trimming.
    """
    if value is None:
        raise ValueError(f"{field_name} is required")

    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")

    return cleaned


def parse_grade(grade_str):
    """Parse and validate a grade value from CLI input.

    Args:
        grade_str (object): Raw grade input, typically a string.

    Returns:
        float: Parsed grade value.

    Raises:
        ValueError: If parsing fails or grade is outside 0-100.
    """
    try:
        grade = float(str(grade_str).strip())
    except (TypeError, ValueError):
        raise ValueError("Grade must be a valid number between 0 and 100")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade