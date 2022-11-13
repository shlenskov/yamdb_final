from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError(
            'Измените имя пользователя.'
        )


class UserRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    message = (
        'Введите корректное имя пользователя. '
        'Максимум 150 символов. '
        'Буквы, цифры и знаки @/./+/-/_ только.'
    )
