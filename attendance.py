"""Attendance calculations for the student attendance report."""


def calculate_attendance_percentage(attended, total):
    """Return attendance as a percentage of classes held, rounded to 2 places.

    Both arguments must be whole numbers of classes (``bool`` is rejected).

    Raises:
        TypeError: if ``attended`` or ``total`` is not an ``int``.
        ValueError: if ``total`` is not positive, ``attended`` is negative,
            or ``attended`` exceeds ``total``.
    """
    for name, value in (("attended", attended), ("total", total)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int, got {type(value).__name__}")

    if total <= 0:
        raise ValueError("total must be greater than 0")
    if attended < 0:
        raise ValueError("attended cannot be negative")
    if attended > total:
        raise ValueError("attended cannot exceed total")

    return round(attended / total * 100, 2)
