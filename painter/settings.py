# -*- coding: utf-8 -*-
import os
from basement import settings
from basement.utils import get_file_path_from_base

BADGE_TEMPLATE_STRING = """
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1" />
    <stop offset="1" stop-opacity=".1" />
  </linearGradient>
  <mask id="a">
    <rect width="{total_width}" height="20" rx="3" fill="#fff" />
  </mask>
  <g mask="url(#a)">
    <path fill="#{key_color}" d="M0 0 h{key_width} v20 H0 z" />
    <path fill="#{value_color}" d="M{key_width} 0 h{value_width} v20 H{key_width} z" />
    <path fill="url(#b)" d="M0 0 h{total_width} v20 H0 z" />
  </g>
  <g fill="#fff" font-family="DejaVu Sans" font-size="11">
    <text x="6" y="15" fill="#010101" fill-opacity=".3">{key_text}</text>
    <text x="6" y="14">{key_text}</text>
    <text x="{value_text_x}" y="15" fill="#010101" fill-opacity=".3">{value_text}</text>
    <text x="{value_text_x}" y="14">{value_text}</text>
  </g>
</svg>
"""

KEY_LEFT_MARGIN = 6
KEY_RIGHT_MARGIN = 4

VALUE_LEFT_MARGIN = 4
VALUE_RIGHT_MARGIN = 6

# COLORS
COLOR_BRIGHT_GREEN = '4c1'
COLOR_GREEN = '97CA00'
COLOR_YELLOW = 'dfb317'
COLOR_YELLOW_GREEN = 'a4a61d'
COLOR_ORANGE = 'fe7d37'
COLOR_RED = 'e05d44'
COLOR_BLUE = '007ec6'
COLOR_GREY = '555'
COLOR_LIGHT_GRAY = '9f9f9f'


FONT_PATH_OPEN_SANS = get_file_path_from_base(
    os.path.join(settings.STATIC_DIR, 'fonts/OpenSans-Regular.ttf')
)
FONT_PATH_DEJAVU_SANS = get_file_path_from_base(
    os.path.join(settings.STATIC_DIR, 'fonts/DejaVuSans.ttf')
)
