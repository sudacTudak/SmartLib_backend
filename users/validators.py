import re
from rest_framework.exceptions import ValidationError


__all__ = ['AppPasswordValidator']

VALID_PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$'
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 30

class AppPasswordValidator:
    min_length: int
    max_length: int

    def __init__(self, /, min_length: int | None = MIN_PASSWORD_LENGTH, max_length: int | None = MAX_PASSWORD_LENGTH):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value):
        trimmed_value = value.strip()
        length = len(trimmed_value)

        if length == 0:
            raise ValidationError('Пароль не может быть пустым')

        if length < self.min_length:
            raise ValidationError(f'Минимальная длина пароля: {self.min_length}')

        if length > self.max_length:
            raise ValidationError(f'Максимальная длина пароля: {self.max_length}')

        if not bool(re.fullmatch(VALID_PASSWORD_PATTERN, value)):
            raise ValidationError('Пароль должен состоять из латинских букв, содержать хотя бы одну заглавную букву и хотя бы одну цифру')
