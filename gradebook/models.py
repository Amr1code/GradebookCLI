class Student:
    def __init__(self, student_id, name):
        if not isinstance(student_id, (int, str)):
            raise ValueError("student_id must be an int or string")
        if isinstance(student_id, str) and not student_id.strip():
            raise ValueError("student_id cannot be empty")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name cannot be empty")

        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    def __init__(self, code, title):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("code cannot be empty")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title cannot be empty")

        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    def __init__(self, student_id, course_code):
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
        if not isinstance(grade, (int, float)):
            raise ValueError("grade must be a number between 0 and 100")
        if grade < 0 or grade > 100:
            raise ValueError("grade must be between 0 and 100")

        self.grades.append(float(grade))

    def __str__(self):
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )