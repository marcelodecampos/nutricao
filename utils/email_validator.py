"""Email validation utility module."""

from email_validator import EmailNotValidError, validate_email


def is_valid_email(email: str) -> bool:
    """
    Validate an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if not email:
        raise ValueError("Email cannot be empty")
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
