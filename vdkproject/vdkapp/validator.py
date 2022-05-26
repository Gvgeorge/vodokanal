from django.core.exceptions import ValidationError
from dateutil.parser import parse


def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


def validate_order_row(row):
    if len(row) != 4:
        raise ValidationError(('%(row)s is not an even number'),
                              params={'row': row},)
    if any(map(lambda x: type(x) != str, row)):
        raise ValidationError('Input params should be strings')

    if not row[0].isnumeric():
        raise ValidationError(f'{row[0]} - value should be numerical')

    if not row[1].isnumeric():
        raise ValidationError(f'{row[1]} - value should be numerical')

    if not is_number(row[2]):
        raise ValidationError(f'{row[2]} - value should be a float/int')

    try:
        date = parse(row[3]).date()
    except ValueError:
        raise ValidationError(f'Wrong date format {date}')
