# -*- coding: utf-8 -*-
import os

from basement.compact import urllib_quote
from basement import settings


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


def get_template_path(template_name):
    """
    :param template_name: Template name
    :type template_name: str

    :rtype: str
    """
    template_path = os.path.join(settings.TEMPLATES_DIR, template_name)

    if not os.path.isfile(template_path):
        raise LookupError('Template file {0} does '
                          'not exists'.format(template_path))

    return template_path


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
