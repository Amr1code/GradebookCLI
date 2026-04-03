import argparse

from gradebook.service import (
	add_course,
	add_grade_to_enrollment,
	add_student,
	compute_student_average,
	compute_student_gpa,
	enroll_student_in_course,
	list_all_courses,
	list_all_students,
	list_enrollments_for_student,
)
from gradebook.storage import load_data, save_data


def build_parser():
	parser = argparse.ArgumentParser(description="Gradebook CLI")
	subparsers = parser.add_subparsers(dest="command", required=True)

	add_student_parser = subparsers.add_parser("add-student", help="Add a student")
	add_student_parser.add_argument("student_id", help="Student id (int or string)")
	add_student_parser.add_argument("name", help="Student full name")

	add_course_parser = subparsers.add_parser("add-course", help="Add a course")
	add_course_parser.add_argument("code", help="Course code")
	add_course_parser.add_argument("title", help="Course title")

	enroll_parser = subparsers.add_parser("enroll", help="Enroll a student in a course")
	enroll_parser.add_argument("student_id", help="Student id")
	enroll_parser.add_argument("course_code", help="Course code")

	add_grade_parser = subparsers.add_parser(
		"add-grade", help="Add a grade to a student enrollment"
	)
	add_grade_parser.add_argument("student_id", help="Student id")
	add_grade_parser.add_argument("course_code", help="Course code")
	add_grade_parser.add_argument("grade", type=float, help="Grade value (0-100)")

	list_parser = subparsers.add_parser("list", help="List students, courses, or enrollments")
	list_parser.add_argument(
		"resource",
		choices=["students", "courses", "enrollments"],
		help="Resource to list",
	)
	list_parser.add_argument(
		"--student-id",
		help="Required when listing enrollments",
	)

	avg_parser = subparsers.add_parser("avg", help="Compute average for a student")
	avg_parser.add_argument("student_id", help="Student id")

	gpa_parser = subparsers.add_parser("gpa", help="Compute GPA for a student")
	gpa_parser.add_argument("student_id", help="Student id")

	return parser


def run_cli(args):
	data = load_data()

	if args.command == "add-student":
		created = add_student(data, args.student_id, args.name)
		print(f"Added student: {created['id']} - {created['name']}")

	elif args.command == "add-course":
		created = add_course(data, args.code, args.title)
		print(f"Added course: {created['code']} - {created['title']}")

	elif args.command == "enroll":
		created = enroll_student_in_course(data, args.student_id, args.course_code)
		print(
			"Enrollment created: "
			f"student={created['student_id']}, course={created['course_code']}"
		)

	elif args.command == "add-grade":
		updated = add_grade_to_enrollment(
			data,
			args.student_id,
			args.course_code,
			args.grade,
		)
		last_grade = updated.get("grades", [])[-1]
		print(
			"Grade added: "
			f"student={updated['student_id']}, "
			f"course={updated['course_code']}, grade={last_grade}"
		)

	elif args.command == "list":
		if args.resource == "students":
			students = list_all_students(data)
			if not students:
				print("No students found.")
			else:
				for student in students:
					print(f"{student['id']}: {student['name']}")

		elif args.resource == "courses":
			courses = list_all_courses(data)
			if not courses:
				print("No courses found.")
			else:
				for course in courses:
					print(f"{course['code']}: {course['title']}")

		elif args.resource == "enrollments":
			if not args.student_id:
				raise ValueError("--student-id is required when listing enrollments")
			enrollments = list_enrollments_for_student(data, args.student_id)
			if not enrollments:
				print(f"No enrollments found for student '{args.student_id}'.")
			else:
				for enrollment in enrollments:
					grades = enrollment.get("grades", [])
					print(f"{enrollment['course_code']}: grades={grades}")

	elif args.command == "avg":
		avg = compute_student_average(data, args.student_id)
		if avg is None:
			print(f"No grades found for student '{args.student_id}'.")
		else:
			print(f"Average for student '{args.student_id}': {avg:.2f}")

	elif args.command == "gpa":
		gpa = compute_student_gpa(data, args.student_id)
		if gpa is None:
			print(f"No grades found for student '{args.student_id}'.")
		else:
			print(f"GPA for student '{args.student_id}': {gpa:.2f}")

	save_data(data)


def main():
	parser = build_parser()
	args = parser.parse_args()

	try:
		run_cli(args)
	except ValueError as exc:
		print(f"Error: {exc}")
	except Exception as exc:
		print(f"Unexpected error: {exc}")


if __name__ == "__main__":
	main()
