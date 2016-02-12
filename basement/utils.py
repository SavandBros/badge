# -*- coding: utf-8 -*-
from basement.compact import urllib_quote


def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


def escape_shield_query(text):
    """Escape text to be inserted in a shield API request."""
    text = urllib_quote(text, safe=' ')
    text = text.replace('_', '__')
    text = text.replace(' ', '_')
    text = text.replace('-', '--')
    return text


intword_converters = (
    (3, lambda number: format_number('%(value).1fk', number)),
    (6, lambda number: format_number('%(value).1fM', number)),
    (9, lambda number: format_number('%(value).1fB', number)),
)
