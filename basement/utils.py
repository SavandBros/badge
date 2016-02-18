# -*- coding: utf-8 -*-
import os

from basement.compact import urllib_quote
from basement import settings


def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


def escape_shield_query(text):
    """Escape text to be inserted in a service_badge API request."""
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


# Pretty much taken straight from Django
def intword(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return str(value)

    for exponent, converters in intword_converters:
        large_number = 10 ** exponent
        if value < large_number * 1000:
            new_value = value / float(large_number)

            return converters(new_value)


def get_file_path_from_base(file_path):
    """
    :param file_path: file path
    :type file_path: str

    :rtype: str
    """
    file_path = os.path.join(settings.BASE_DIR, file_path)

    if not os.path.isfile(file_path):
        raise LookupError('File {0} does not exists'.format(file_path))

    return file_path


def get_template_path(template_name):
    """
    :param template_name: Template name
    :type template_name: str

    :rtype: str
    """
    return get_file_path_from_base(
        os.path.join(settings.TEMPLATE_DIR_NAME, template_name)
    )


def render_to_string(template_name):
    """
    Return a string of template name.

    :param template_name: Template name
    :type template_name: str

    :rtype: str
    """
    with open(get_template_path(template_name), 'r') as tfile:
        return tfile.read()


def render_template(template_name):
    """
    Return a string of template name.

    :param template_name: Template name
    :type template_name: str

    :rtype: str
    """
    return render_to_string(template_name)
