"""Attendance summary: prints each student's attendance percentage and status.

Exits with a non-zero status if any record is invalid, so CI fails on bad data.
Low attendance is reported but does not fail the run.
"""
import sys

from attendance import calculate_attendance_percentage

MINIMUM_PERCENTAGE = 75.0

# (student, classes attended, classes held)
RECORDS = [
    ("Aarav Sharma", 40, 40),
    ("Diya Patel", 34, 40),
    ("Kabir Singh", 28, 40),
    ("Meera Nair", 0, 40),
]


def build_summary(records, minimum=MINIMUM_PERCENTAGE):
    """Return (student, attended, total, percentage, status) for each record."""
    rows = []
    for student, attended, total in records:
        percentage = calculate_attendance_percentage(attended, total)
        status = "OK" if percentage >= minimum else "LOW"
        rows.append((student, attended, total, percentage, status))
    return rows


def main():
    try:
        rows = build_summary(RECORDS)
    except (TypeError, ValueError) as error:
        print(f"Invalid attendance record: {error}", file=sys.stderr)
        return 1

    print(f"{'Student':<15}{'Attended':>9}{'Total':>7}{'Percent':>9}  Status")
    for student, attended, total, percentage, status in rows:
        print(f"{student:<15}{attended:>9}{total:>7}{percentage:>8.2f}%  {status}")

    low = sum(1 for row in rows if row[4] == "LOW")
    print(f"\n{len(rows)} students, {low} below {MINIMUM_PERCENTAGE:g}%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
