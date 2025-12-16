"""
Core Utilities
Shared utility functions for all managers
Location: core/utils.py
"""
import hashlib
import uuid
from datetime import datetime, date
from typing import Optional, Union


def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID with optional prefix
    
    Args:
        prefix: Optional prefix for the ID (e.g., "V" for visit, "LAB" for lab)
    
    Returns:
        str: Unique ID string
    
    Example:
        >>> generate_id("V")
        'VA1B2C3D4'
        >>> generate_id("LAB")
        'LAB5E6F7G8'
    """
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"


def hash_password(password: str) -> str:
    """
    Hash password using SHA-256
    
    Args:
        password: Plain text password
    
    Returns:
        str: Hashed password
    
    Example:
        >>> hash_password("mypassword123")
        '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0'
    """
    return hashlib.sha256(password.encode()).hexdigest()


def parse_date(date_str: Optional[str], format: str = "%Y-%m-%d") -> Optional[date]:
    """
    Parse date string to date object
    
    Args:
        date_str: Date string to parse
        format: Date format (default: YYYY-MM-DD)
    
    Returns:
        date object or None if parsing fails
    
    Example:
        >>> parse_date("2024-01-15")
        datetime.date(2024, 1, 15)
        >>> parse_date("invalid")
        None
    """
    if not date_str:
        return None
    
    try:
        return datetime.strptime(date_str, format).date()
    except (ValueError, TypeError):
        return None


def parse_datetime(datetime_str: Optional[str], format: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Parse datetime string to datetime object
    
    Args:
        datetime_str: Datetime string to parse
        format: Datetime format (default: YYYY-MM-DD HH:MM:SS)
    
    Returns:
        datetime object or None if parsing fails
    
    Example:
        >>> parse_datetime("2024-01-15 14:30:00")
        datetime.datetime(2024, 1, 15, 14, 30)
        >>> parse_datetime("invalid")
        None
    """
    if not datetime_str:
        return None
    
    try:
        return datetime.strptime(datetime_str, format)
    except (ValueError, TypeError):
        return None


def validate_national_id(national_id: Optional[str]) -> bool:
    """
    Validate Egyptian national ID (14 digits)
    
    Args:
        national_id: National ID string to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Example:
        >>> validate_national_id("29501012345678")
        True
        >>> validate_national_id("123")
        False
        >>> validate_national_id("abcd1234567890")
        False
    """
    if not national_id:
        return False
    
    # Must be exactly 14 digits
    if len(national_id) != 14:
        return False
    
    # Must contain only digits
    if not national_id.isdigit():
        return False
    
    return True


def calculate_age(date_of_birth: Optional[Union[date, str]]) -> Optional[int]:
    """
    Calculate age from date of birth
    
    Args:
        date_of_birth: Date of birth (date object or string)
    
    Returns:
        int: Age in years, or None if invalid
    
    Example:
        >>> from datetime import date
        >>> calculate_age(date(2000, 1, 1))
        24  # (assuming current year is 2024)
        >>> calculate_age("2000-01-01")
        24
        >>> calculate_age(None)
        None
    """
    if not date_of_birth:
        return None
    
    # Convert string to date if needed
    if isinstance(date_of_birth, str):
        date_of_birth = parse_date(date_of_birth)
        if not date_of_birth:
            return None
    
    today = datetime.now().date()
    
    # Calculate age
    age = today.year - date_of_birth.year
    
    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1
    
    return age


def validate_email(email: Optional[str]) -> bool:
    """
    Basic email validation
    
    Args:
        email: Email string to validate
    
    Returns:
        bool: True if valid format, False otherwise
    
    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
        >>> validate_email(None)
        False
    """
    if not email:
        return False
    
    # Basic validation: contains @ and .
    if '@' not in email or '.' not in email:
        return False
    
    # Split by @
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    # Local part should not be empty
    if not local:
        return False
    
    # Domain should have at least one dot
    if '.' not in domain:
        return False
    
    return True


def validate_phone(phone: Optional[str]) -> bool:
    """
    Validate Egyptian phone number
    
    Args:
        phone: Phone number string to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Example:
        >>> validate_phone("01012345678")
        True
        >>> validate_phone("0201234567890")
        True
        >>> validate_phone("123")
        False
    """
    if not phone:
        return False
    
    # Remove spaces and dashes
    clean_phone = phone.replace(' ', '').replace('-', '')
    
    # Egyptian mobile: 11 digits starting with 01
    if len(clean_phone) == 11 and clean_phone.startswith('01'):
        return clean_phone.isdigit()
    
    # Egyptian landline with country code: 13 digits starting with 002
    if len(clean_phone) == 13 and clean_phone.startswith('002'):
        return clean_phone.isdigit()
    
    # Egyptian landline: 10 digits starting with 0
    if len(clean_phone) == 10 and clean_phone.startswith('0'):
        return clean_phone.isdigit()
    
    return False


def format_date(date_obj: Optional[Union[date, datetime]], format: str = "%Y-%m-%d") -> Optional[str]:
    """
    Format date object to string
    
    Args:
        date_obj: Date or datetime object
        format: Output format (default: YYYY-MM-DD)
    
    Returns:
        str: Formatted date string, or None if invalid
    
    Example:
        >>> from datetime import date
        >>> format_date(date(2024, 1, 15))
        '2024-01-15'
        >>> format_date(None)
        None
    """
    if not date_obj:
        return None
    
    try:
        if isinstance(date_obj, datetime):
            return date_obj.strftime(format)
        elif isinstance(date_obj, date):
            return date_obj.strftime(format)
        else:
            return None
    except (ValueError, AttributeError):
        return None


def sanitize_string(text: Optional[str], max_length: Optional[int] = None) -> str:
    """
    Sanitize string input (remove extra whitespace, trim)
    
    Args:
        text: String to sanitize
        max_length: Optional maximum length
    
    Returns:
        str: Sanitized string
    
    Example:
        >>> sanitize_string("  Hello   World  ")
        'Hello World'
        >>> sanitize_string("Long text", max_length=5)
        'Long '
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = text.strip()
    
    # Replace multiple spaces with single space
    sanitized = ' '.join(sanitized.split())
    
    # Trim to max length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_blood_type(blood_type: Optional[str]) -> bool:
    """
    Validate blood type
    
    Args:
        blood_type: Blood type string to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Example:
        >>> validate_blood_type("A+")
        True
        >>> validate_blood_type("O-")
        True
        >>> validate_blood_type("XY")
        False
    """
    if not blood_type:
        return False
    
    valid_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return blood_type in valid_types


def get_gender_display(gender: Optional[str]) -> str:
    """
    Get display name for gender code
    
    Args:
        gender: Gender code (M/F/Male/Female)
    
    Returns:
        str: Display name
    
    Example:
        >>> get_gender_display("M")
        'Male'
        >>> get_gender_display("Female")
        'Female'
    """
    if not gender:
        return "Unknown"
    
    gender_upper = gender.upper()
    
    if gender_upper in ["M", "MALE"]:
        return "Male"
    elif gender_upper in ["F", "FEMALE"]:
        return "Female"
    else:
        return gender


def is_valid_role(role: Optional[str]) -> bool:
    """
    Check if role is valid
    
    Args:
        role: Role string to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Example:
        >>> is_valid_role("doctor")
        True
        >>> is_valid_role("invalid")
        False
    """
    if not role:
        return False
    
    valid_roles = ["doctor", "patient", "admin", "nurse"]
    return role.lower() in valid_roles


# Export all functions
__all__ = [
    'generate_id',
    'hash_password',
    'parse_date',
    'parse_datetime',
    'validate_national_id',
    'calculate_age',
    'validate_email',
    'validate_phone',
    'format_date',
    'sanitize_string',
    'validate_blood_type',
    'get_gender_display',
    'is_valid_role'
]