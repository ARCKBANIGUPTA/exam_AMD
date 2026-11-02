import pytest

from attendance import calculate_attendance_percentage


def test_full_attendance_is_100_percent():
    assert calculate_attendance_percentage(40, 40) == 100.0


@pytest.mark.parametrize(
    "attended, total, expected",
    [
        (34, 40, 85.0),
        (28, 40, 70.0),
        (1, 2, 50.0),
        (1, 3, 33.33),  # rounded to 2 decimal places
        (2, 3, 66.67),
    ],
)
def test_partial_attendance(attended, total, expected):
    assert calculate_attendance_percentage(attended, total) == expected


@pytest.mark.parametrize("total", [1, 40, 200])
def test_zero_attendance_is_0_percent(total):
    result = calculate_attendance_percentage(0, total)
    assert result == 0.0
    assert isinstance(result, float)


@pytest.mark.parametrize(
    "attended, total",
    [
        (5, 0),    # no classes held -> would divide by zero
        (5, -10),  # negative total
        (-1, 10),  # negative attended
        (11, 10),  # attended more than held
    ],
)
def test_out_of_range_values_raise_value_error(attended, total):
    with pytest.raises(ValueError):
        calculate_attendance_percentage(attended, total)


@pytest.mark.parametrize(
    "attended, total",
    [
        ("5", 10),
        (5, "10"),
        (None, 10),
        (5, None),
        (7.5, 10),
        (True, 10),  # bool is an int subclass but not a valid count
    ],
)
def test_non_integer_values_raise_type_error(attended, total):
    with pytest.raises(TypeError):
        calculate_attendance_percentage(attended, total)
