from django.core.exceptions import ValidationError


def min_share_count_validator(value):
    if value <= 0:
        raise ValidationError('Ensure the count of shares is greater than 0')
