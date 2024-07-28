from django.core.exceptions import ValidationError
import re

def validate_mobile(value):
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError(
            ('Mobile number must be exactly 10 digits long.'),
            params={'value': value},
        )