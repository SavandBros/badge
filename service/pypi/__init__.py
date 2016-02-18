# -*- coding: utf-8 -*-
"""
PyPi
====

Everything around PyPi
"""

import requests
from yarg.package import json2package

from basement.settings import redis
from basement.utils import escape_shield_query, intword
from basement import settings
from painter import settings as painter_settings
from service.base import ServiceBase



        if r_data:
        else:


    def get_implementations(self):
        """
        cs = [c.lower() for c in cs]
        if not len(cs) > 0:
        return cs

    def get_status(self):
            return "none found"

            if classifier.startswith("Development Status"):
                bits = classifier.split(' :: ')
                return bits[1].split(' - ')
        return "1", "unknown"

    def get_license(self):
        statuses = {
            '1': painter_settings.COLOR_RED,
            '2': painter_settings.COLOR_RED,
            '3': painter_settings.COLOR_RED,
            '4': painter_settings.COLOR_YELLOW,
            '5': painter_settings.COLOR_BRIGHT_GREEN,
            '6': painter_settings.COLOR_BRIGHT_GREEN,
            '7': painter_settings.COLOR_RED
        }
        code, status = self.get_status()
        status = status.lower().replace('-', '--')
        status = "stable" if status == "production/stable" else status

