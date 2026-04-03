from .models import Course, Enrollment, Student


def add_student(data, student_id, name):
    """Add a new student record to the data dictionary.

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Unique student identifier.
        name (str): Student display name.

    Returns:
        dict: The created student record.

    Raises:
        ValueError: If the student already exists or input is invalid.
    """
    students = data.setdefault("students", [])
    existing_students = {student["id"]: student for student in students if "id" in student}
    if student_id in existing_students:
        raise ValueError(f"Student with id '{student_id}' already exists")

    student = Student(student_id, name)
    student_record = {"id": student.id, "name": student.name}
    students.append(student_record)
    return student_record


def add_course(data, code, title):
    """Add a new course record to the data dictionary.

    Args:
        data (dict): Main gradebook dictionary.
        code (str): Unique course code.
        title (str): Course title.

    Returns:
        dict: The created course record.

    Raises:
        ValueError: If the course already exists or input is invalid.
    """
    courses = data.setdefault("courses", [])
    existing_courses = {course["code"]: course for course in courses if "code" in course}
    if code in existing_courses:
        raise ValueError(f"Course with code '{code}' already exists")

    course = Course(code, title)
    course_record = {"code": course.code, "title": course.title}
    courses.append(course_record)
    return course_record


def enroll_student_in_course(data, student_id, course_code):
    """Create an enrollment between an existing student and course.

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Student identifier.
        course_code (str): Course code.

    Returns:
        dict: The created enrollment record.

    Raises:
        ValueError: If the student or course does not exist, or enrollment exists.
    """
    students = data.setdefault("students", [])
    courses = data.setdefault("courses", [])
    enrollments = data.setdefault("enrollments", [])

    matching_students = [student for student in students if student.get("id") == student_id]
    if not matching_students:
        raise ValueError(f"Student '{student_id}' does not exist")

    matching_courses = [course for course in courses if course.get("code") == course_code]
    if not matching_courses:
        raise ValueError(f"Course '{course_code}' does not exist")

    existing_enrollments = [
        enrollment
        for enrollment in enrollments
        if enrollment.get("student_id") == student_id
        and enrollment.get("course_code") == course_code
    ]
    if existing_enrollments:
        raise ValueError(
            f"Student '{student_id}' is already enrolled in course '{course_code}'"
        )

    enrollment = Enrollment(student_id, course_code)
    enrollment_record = {
        "student_id": enrollment.student_id,
        "course_code": enrollment.course_code,
        "grades": list(enrollment.grades),
    }
    enrollments.append(enrollment_record)
    return enrollment_record


def add_grade_to_enrollment(data, student_id, course_code, grade):
    """Add a validated grade to an existing enrollment.

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Student identifier.
        course_code (str): Course code.
        grade (int | float): Grade value between 0 and 100.

    Returns:
        dict: The updated enrollment record.

    Raises:
        ValueError: If enrollment is missing or grade is invalid.
    """
    enrollments = data.setdefault("enrollments", [])
    matching_enrollments = [
        enrollment
        for enrollment in enrollments
        if enrollment.get("student_id") == student_id
        and enrollment.get("course_code") == course_code
    ]
    if not matching_enrollments:
        raise ValueError(
            f"Enrollment for student '{student_id}' in course '{course_code}' not found"
        )

    grade_validator = Enrollment(student_id, course_code)
    grade_validator.add_grade(grade)
    validated_grade = grade_validator.grades[0]

    matching_enrollments[0].setdefault("grades", []).append(validated_grade)
    return matching_enrollments[0]


def list_all_students(data):
    """Return all students sorted alphabetically by name.

    Args:
        data (dict): Main gradebook dictionary.

    Returns:
        list[dict]: Student records with id and name keys.
    """
    students = [
        {"id": student.get("id"), "name": student.get("name", "")}
        for student in data.get("students", [])
    ]
    return sorted(students, key=lambda student: student["name"].lower())


def list_all_courses(data):
    """Return all courses sorted by course code.

    Args:
        data (dict): Main gradebook dictionary.

    Returns:
        list[dict]: Course records with code and title keys.
    """
    courses = [
        {"code": course.get("code", ""), "title": course.get("title", "")}
        for course in data.get("courses", [])
    ]
    return sorted(courses, key=lambda course: course["code"].lower())


def list_enrollments_for_student(data, student_id):
    """Return all enrollments for a student sorted by course code.

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Student identifier.

    Returns:
        list[dict]: Enrollment records for the specified student.
    """
    enrollments = [
        enrollment
        for enrollment in data.get("enrollments", [])
        if enrollment.get("student_id") == student_id
    ]
    return sorted(enrollments, key=lambda enrollment: enrollment.get("course_code", ""))


def compute_student_average(data, student_id):
    """Compute the arithmetic mean of all grades for a student.

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Student identifier.

    Returns:
        float | None: Average grade, or None when the student has no grades.
    """
    grades = [
        grade
        for enrollment in data.get("enrollments", [])
        if enrollment.get("student_id") == student_id
        for grade in enrollment.get("grades", [])
    ]
    if not grades:
        return None

    return sum(grades) / len(grades)


def compute_student_gpa(data, student_id):
    """Compute GPA on a 0.0-4.0 scale from a student's average grade.

    The current mapping is linear: GPA = average / 25, clamped to [0.0, 4.0].

    Args:
        data (dict): Main gradebook dictionary.
        student_id (int | str): Student identifier.

    Returns:
        float | None: GPA rounded to two decimals, or None if no grades exist.
    """
    average = compute_student_average(data, student_id)
    if average is None:
        return None

    gpa = max(0.0, min(4.0, average / 25.0))
    return round(gpa, 2)