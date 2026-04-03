class Student:
    """Represent a student in the gradebook domain.

    Attributes:
        id (int | str): Unique student identifier.
        name (str): Student display name.
    """

    def __init__(self, student_id, name):
        """Initialize a student.

        Args:
            student_id (int | str): Unique student identifier.
            name (str): Student name.

        Raises:
            ValueError: If the identifier type is invalid or values are empty.
        """
        if not isinstance(student_id, (int, str)):
            raise ValueError("student_id must be an int or string")
        if isinstance(student_id, str) and not student_id.strip():
            raise ValueError("student_id cannot be empty")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name cannot be empty")

        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        """Return a readable student representation."""
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    """Represent a course that students can enroll in.

    Attributes:
        code (str): Course identifier such as CS101.
        title (str): Human-readable course title.
    """

    def __init__(self, code, title):
        """Initialize a course.

        Args:
            code (str): Course identifier.
            title (str): Course title.

        Raises:
            ValueError: If code or title is empty.
        """
        if not isinstance(code, str) or not code.strip():
            raise ValueError("code cannot be empty")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title cannot be empty")

        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        """Return a readable course representation."""
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    """Represent a student enrollment in a single course.

    Attributes:
        student_id (int | str): The enrolled student identifier.
        course_code (str): The enrolled course code.
        grades (list[float]): Grade values between 0 and 100.
    """

    def __init__(self, student_id, course_code):
        """Initialize an enrollment record.

        Args:
            student_id (int | str): Student identifier.
            course_code (str): Course code.

        Raises:
            ValueError: If any required identifier is invalid or empty.
        """
        if not isinstance(student_id, (int, str)):
            raise ValueError("student_id must be an int or string")
        if isinstance(student_id, str) and not student_id.strip():
            raise ValueError("student_id cannot be empty")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("course_code cannot be empty")

        self.student_id = student_id
        self.course_code = course_code.strip()
        self.grades = []

    def add_grade(self, grade):
        """Validate and append a grade.

        Args:
            grade (int | float): Grade to append.

        Raises:
            ValueError: If grade is not numeric or outside 0-100.
        """
        if not isinstance(grade, (int, float)):
            raise ValueError("grade must be a number between 0 and 100")
        if grade < 0 or grade > 100:
            raise ValueError("grade must be between 0 and 100")

        self.grades.append(float(grade))

    def __str__(self):
        """Return a readable enrollment representation."""
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )