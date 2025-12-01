"""
Date utility functions for MedLink
Provides age calculation and date formatting utilities
Location: utils/date_utils.py
"""
from datetime import datetime, timedelta
from typing import Optional


def calculate_age(date_of_birth: str) -> int:
    """
    Calculate age from date of birth string

    Args:
        date_of_birth: Date string in format 'YYYY-MM-DD'

    Returns:
        Age in years as integer

    Example:
        >>> calculate_age('1995-01-01')
        29
    """
    try:
        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
        today = datetime.now()

        # Calculate age
        age = today.year - birth_date.year

        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age
    except (ValueError, AttributeError):
        return 0


def format_date(date_str: str, input_format: str = '%Y-%m-%d', output_format: str = '%d/%m/%Y') -> str:
    """
    Format date string from one format to another

    Args:
        date_str: Input date string
        input_format: Format of input date (default: YYYY-MM-DD)
        output_format: Desired output format (default: DD/MM/YYYY)

    Returns:
        Formatted date string

    Example:
        >>> format_date('2024-11-28')
        '28/11/2024'
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except (ValueError, AttributeError):
        return date_str


def get_current_date(format_str: str = '%Y-%m-%d') -> str:
    """
    Get current date in specified format

    Args:
        format_str: Desired date format (default: YYYY-MM-DD)

    Returns:
        Current date string

    Example:
        >>> get_current_date()
        '2024-11-28'
    """
    return datetime.now().strftime(format_str)


def get_current_datetime(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Get current date and time in specified format

    Args:
        format_str: Desired datetime format (default: YYYY-MM-DD HH:MM:SS)

    Returns:
        Current datetime string

    Example:
        >>> get_current_datetime()
        '2024-11-28 10:30:45'
    """
    return datetime.now().strftime(format_str)


def validate_date(date_str: str, format_str: str = '%Y-%m-%d') -> bool:
    """
    Validate if string is a valid date in given format

    Args:
        date_str: Date string to validate
        format_str: Expected date format

    Returns:
        True if valid date, False otherwise

    Example:
        >>> validate_date('2024-11-28')
        True
        >>> validate_date('2024-13-01')
        False
    """
    try:
        datetime.strptime(date_str, format_str)
        return True
    except (ValueError, AttributeError):
        return False


def date_difference_days(date1: str, date2: str, format_str: str = '%Y-%m-%d') -> int:
    """
    Calculate difference in days between two dates

    Args:
        date1: First date string
        date2: Second date string
        format_str: Date format for both dates

    Returns:
        Number of days between dates (positive if date2 > date1)

    Example:
        >>> date_difference_days('2024-11-01', '2024-11-28')
        27
    """
    try:
        d1 = datetime.strptime(date1, format_str)
        d2 = datetime.strptime(date2, format_str)
        return (d2 - d1).days
    except (ValueError, AttributeError):
        return 0


def add_days(date_str: str, days: int, format_str: str = '%Y-%m-%d') -> str:
    """
    Add specified number of days to a date

    Args:
        date_str: Starting date string
        days: Number of days to add (negative to subtract)
        format_str: Date format

    Returns:
        New date string after adding days

    Example:
        >>> add_days('2024-11-28', 7)
        '2024-12-05'
    """
    try:
        date_obj = datetime.strptime(date_str, format_str)
        new_date = date_obj + timedelta(days=days)
        return new_date.strftime(format_str)
    except (ValueError, AttributeError):
        return date_str


def is_date_in_past(date_str: str, format_str: str = '%Y-%m-%d') -> bool:
    """
    Check if date is in the past

    Args:
        date_str: Date string to check
        format_str: Date format

    Returns:
        True if date is in the past, False otherwise

    Example:
        >>> is_date_in_past('2020-01-01')
        True
    """
    try:
        date_obj = datetime.strptime(date_str, format_str)
        return date_obj < datetime.now()
    except (ValueError, AttributeError):
        return False


def is_date_in_future(date_str: str, format_str: str = '%Y-%m-%d') -> bool:
    """
    Check if date is in the future

    Args:
        date_str: Date string to check
        format_str: Date format

    Returns:
        True if date is in the future, False otherwise

    Example:
        >>> is_date_in_future('2025-01-01')
        True
    """
    try:
        date_obj = datetime.strptime(date_str, format_str)
        return date_obj > datetime.now()
    except (ValueError, AttributeError):
        return False


def get_age_group(age: int) -> str:
    """
    Get age group category for a given age

    Args:
        age: Age in years

    Returns:
        Age group string

    Example:
        >>> get_age_group(25)
        'Young Adult'
    """
    if age < 0:
        return "Invalid"
    elif age <= 2:
        return "Infant"
    elif age <= 12:
        return "Child"
    elif age <= 19:
        return "Adolescent"
    elif age <= 35:
        return "Young Adult"
    elif age <= 55:
        return "Middle-aged Adult"
    elif age <= 70:
        return "Older Adult"
    else:
        return "Elderly"


def format_date_arabic(date_str: str, format_str: str = '%Y-%m-%d') -> str:
    """
    Format date with Arabic month names

    Args:
        date_str: Date string
        format_str: Input date format

    Returns:
        Date formatted with Arabic month names

    Example:
        >>> format_date_arabic('2024-11-28')
        '28 نوفمبر 2024'
    """
    arabic_months = {
        1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
        5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
        9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
    }

    try:
        date_obj = datetime.strptime(date_str, format_str)
        month_arabic = arabic_months[date_obj.month]
        return f"{date_obj.day} {month_arabic} {date_obj.year}"
    except (ValueError, AttributeError, KeyError):
        return date_str


def is_valid_date(date_str: str) -> bool:
    """Check if date string is valid"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

# For backwards compatibility


def get_age_from_dob(dob: str) -> int:
    """
    Alias for calculate_age for backwards compatibility

    Args:
        dob: Date of birth string in format 'YYYY-MM-DD'

    Returns:
        Age in years
    """
    return calculate_age(dob)

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

if __name__ == "__main__":
    # Test functions
    print("Testing date utilities:")
    print(f"Age from 1995-01-01: {calculate_age('1995-01-01')}")
    print(f"Current date: {get_current_date()}")
    print(f"Current datetime: {get_current_datetime()}")
    print(f"Formatted date: {format_date('2024-11-28')}")
    print(f"Age group for 25: {get_age_group(25)}")
    print(f"Arabic date: {format_date_arabic('2024-11-28')}")
