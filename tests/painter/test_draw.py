# -*- coding: utf-8 -*-
from unittest import TestCase
from painter import settings

from painter.draw import Draw


class TestDraw(TestCase):
    painter_badge_kloud51_brightgreen = """
<svg xmlns="http://www.w3.org/2000/svg" width="93.359375" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1" />
    <stop offset="1" stop-opacity=".1" />
  </linearGradient>
  <mask id="a">
    <rect width="93.359375" height="20" rx="3" fill="#fff" />
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0 h42.375 v20 H0 z" />
    <path fill="#4c1" d="M42.375 0 h50.984375 v20 H42.375 z" />
    <path fill="url(#b)" d="M0 0 h93.359375 v20 H0 z" />
  </g>
  <g fill="#fff" font-family="Open Sans" font-size="11">
    <text x="6" y="15" fill="#010101" fill-opacity=".3">badge</text>
    <text x="6" y="14">badge</text>
    <text x="46.375" y="15" fill="#010101" fill-opacity=".3">kloud51</text>
    <text x="46.375" y="14">kloud51</text>
  </g>
</svg>
"""

    def test_draw_badge(self):
        draw = Draw('badge', settings.COLOR_BRIGHT_GREEN, 'kloud51')
        svg_text = draw.as_svg()

        self.assertEqual(svg_text, self.painter_badge_kloud51_brightgreen)
