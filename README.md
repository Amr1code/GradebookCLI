# Gradebook CLI

Gradebook CLI is a command-line Python application for managing students, courses, enrollments, and grades. It stores data in a JSON file and supports average and GPA calculations through simple subcommands.

## Setup

1. Clone the repository and move into the project directory.
2. Create and activate a virtual environment.
3. Run the CLI help command to verify the project runs.

### Bash/Zsh

```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py --help
```

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python main.py --help
```

Optional verification:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Seed Mock Data

Run the seeding script to populate `data/gradebook.json` with sample Albanian students, courses, enrollments, and grades.

```bash
python scripts/seed.py
```

Expected output:

```text
Seed data created successfully at data/gradebook.json
```

## Usage

The examples below assume the virtual environment is active.

### 1. Add a student

```bash
python main.py add-student s10 Lorik
```

Expected output:

```text
Added student: s10 - Lorik
```

### 2. Enroll a student in a course

```bash
python main.py enroll s1 MAT101
```

Expected output:

```text
Enrollment created: student=s1, course=MAT101
```

### 3. Get student GPA

```bash
python main.py gpa s1
```

Expected output format:

```text
GPA for student 's1': 3.60
```

Note: the GPA value depends on grades currently stored in `data/gradebook.json`.

## Design Decisions and Limitations

- Storage format: JSON was chosen for assignment simplicity, human readability, and zero external dependencies.
- Service layer design: business logic is implemented with pure functions operating on a shared in-memory dictionary, which keeps behavior easy to test.
- Limitations:
  - No concurrent write protection or file locking for multi-process access.
  - No database indexing or query optimization for large datasets.
  - No authentication, authorization, or audit model.
  - Schema validation is minimal and enforced mainly by application logic.
  - CLI interactions are synchronous and single-user.