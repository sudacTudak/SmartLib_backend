import re
from rest_framework.exceptions import ValidationError

__all__ = ['password_validator']

VALID_PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$'

def password_validator(value: str):
    trimmed_value = value.strip()

    if not trimmed_value:
        raise ValidationError('Empty password is not allowed')

    if not bool(re.fullmatch(VALID_PASSWORD_PATTERN, value)):
        raise ValidationError('Wrong password content')