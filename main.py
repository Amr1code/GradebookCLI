import argparse
import logging
import os

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
from gradebook.validators import parse_grade, parse_non_empty


def configure_logging(log_filepath="logs/app.log"):
	log_dir = os.path.dirname(log_filepath)
	if log_dir:
		os.makedirs(log_dir, exist_ok=True)

	logging.basicConfig(
		filename=log_filepath,
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s",
	)


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
	add_grade_parser.add_argument("grade", help="Grade value (0-100)")

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
		student_id = parse_non_empty(args.student_id, "student_id")
		name = parse_non_empty(args.name, "name")
		created = add_student(data, student_id, name)
		print(f"Added student: {created['id']} - {created['name']}")

	elif args.command == "add-course":
		code = parse_non_empty(args.code, "code")
		title = parse_non_empty(args.title, "title")
		created = add_course(data, code, title)
		print(f"Added course: {created['code']} - {created['title']}")

	elif args.command == "enroll":
		student_id = parse_non_empty(args.student_id, "student_id")
		course_code = parse_non_empty(args.course_code, "course_code")
		created = enroll_student_in_course(data, student_id, course_code)
		print(
			"Enrollment created: "
			f"student={created['student_id']}, course={created['course_code']}"
		)

	elif args.command == "add-grade":
		student_id = parse_non_empty(args.student_id, "student_id")
		course_code = parse_non_empty(args.course_code, "course_code")
		grade = parse_grade(args.grade)
		updated = add_grade_to_enrollment(
			data,
			student_id,
			course_code,
			grade,
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
			student_id = parse_non_empty(args.student_id, "--student-id")
			enrollments = list_enrollments_for_student(data, student_id)
			if not enrollments:
				print(f"No enrollments found for student '{student_id}'.")
			else:
				for enrollment in enrollments:
					grades = enrollment.get("grades", [])
					print(f"{enrollment['course_code']}: grades={grades}")

	elif args.command == "avg":
		student_id = parse_non_empty(args.student_id, "student_id")
		avg = compute_student_average(data, student_id)
		if avg is None:
			print(f"No grades found for student '{student_id}'.")
		else:
			print(f"Average for student '{student_id}': {avg:.2f}")

	elif args.command == "gpa":
		student_id = parse_non_empty(args.student_id, "student_id")
		gpa = compute_student_gpa(data, student_id)
		if gpa is None:
			print(f"No grades found for student '{student_id}'.")
		else:
			print(f"GPA for student '{student_id}': {gpa:.2f}")

	save_data(data)


def main():
	configure_logging()
	logging.info("Gradebook CLI started")

	parser = build_parser()
	args = parser.parse_args()

	try:
		run_cli(args)
		logging.info("Command executed successfully: %s", args.command)
	except ValueError as exc:
		logging.error("Validation error during CLI execution", exc_info=True)
		print(f"Error: {exc}")
	except Exception as exc:
		logging.error("Unexpected CLI error", exc_info=True)
		print(f"Unexpected error: {exc}")


if __name__ == "__main__":
	main()
