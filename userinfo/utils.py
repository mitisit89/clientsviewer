from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def email_is_valid(value: str) -> tuple[bool, str]:
    """Validate a single email."""
    message_invalid = "Enter a valid email address."

    if not value:
        return False, message_invalid
    try:
        validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ""
