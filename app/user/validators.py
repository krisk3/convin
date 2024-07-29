from django.core.exceptions import ValidationError
import re

def validate_mobile(value):
    """Validator to check whether the mobile number contains 10 digits."""
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError(
            ('Mobile number must be exactly 10 digits long.'),
            params={'value': value},
        )