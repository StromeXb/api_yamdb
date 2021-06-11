import datetime as dt

from django.core.exceptions import ValidationError


def pub_year_validator(value):
    if value < 800 or value > dt.datetime.now().year + 10:
        raise ValidationError(
            'Некорректный год создания!',
            params={'value': value},
        )
