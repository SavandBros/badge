# -*- coding: utf-8 -*-
"""
Draw
====

Simply drawing SVG from given attributes.
It can draw as:

* SVG
* PNG
"""
from wand.drawing import Drawing
from wand.image import Image

from painter import settings


class Draw(object):
    key_color = None
    key_text = None
    key_text_width = None
    key_width = None
    value_color = None
    value_text = None
    value_text_width = None
    value_width = None
    value_text_x = None
    total_width = None
    font = settings.FONT_PATH_OPEN_SANS
    font_size = 11
    _canvas = None

    def __init__(self, key_text, value_color, value_text, key_color=settings.COLOR_GREY):
        self.key_text = key_text
        self.value_color = value_color
        self.value_text = value_text
        self.key_color = key_color

        self._canvas = Image(width=1, height=1)

    def get_key_text_width(self):
        """
        :rtype: int
        """
        if not self.key_text_width:
            self.key_text_width = self.get_text_width(self.key_text)

        return self.key_text_width

    def get_key_width(self):
        """
        :rtype: int
        """
        if not self.key_width:
            self.key_width = (
                settings.KEY_LEFT_MARGIN +
                self.get_key_text_width() +
                settings.KEY_RIGHT_MARGIN
            )

        return self.key_width

    def get_value_text_width(self):
        """
        :rtype: int
        """
        if not self.value_text_width:
            self.value_text_width = self.get_text_width(self.value_text)

        return self.value_text_width

    def get_value_text_x(self):
        """
        :rtype: int
        """
        if not self.value_text_x:
            self.value_text_x = (self.get_key_width() +
                                 settings.VALUE_LEFT_MARGIN)

        return self.value_text_x

    def get_value_width(self):
        """
        :rtype: int
        """
        if not self.value_width:
            self.value_width = (
                settings.VALUE_LEFT_MARGIN +
                self.get_value_text_width() +
                settings.VALUE_RIGHT_MARGIN
            )

        return self.value_width

    def get_total_width(self):
        """
        :rtype: int
        """
        if not self.total_width:
            self.total_width = (self.get_key_width() + self.get_value_width())

        return self.total_width

    def get_text_width(self, text):
        """
        :rtype: int
        """
        with Drawing() as painter:
            painter.font = self.font
            painter.font_size = self.font_size
            font_metrics = painter.get_font_metrics(self._canvas, text=text)

            return font_metrics.text_width

    def as_svg(self):
        """
        <3

        :rtype: str
        """
        return settings.BADGE_TEMPLATE_STRING.format(
            total_width=self.get_total_width(),
            key_color=self.key_color,
            key_width=self.get_key_width(),
            key_text=self.key_text,
            value_color=self.value_color,
            value_text_x=self.get_value_text_x(),
            value_text=self.value_text,
            value_width=self.get_value_width()
        )

    def as_png(self):
        """
        :type
        """
        svg = self.as_svg()

        with Image(blob=svg, format="svg") as image:
                return image.make_blob('png')
