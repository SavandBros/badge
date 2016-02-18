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


class PyPiService(ServiceBase):
    """
    Get the pypi json data for the package #fuck, and process.
    """
    def pull_package_data(self):
        """
        :rtype: dict
        """
        pkg_url = settings.PYPI_URL % self.package_name
        r_data = redis.get(self.package_name)

        if r_data:
            self.package_data = json2package(r_data)

        response = requests.get(pkg_url)

        if 400 <= response.status_code < 500 or 500 <= response.status_code < 600:
            self.set_package_pulling_failed()
        else:
            redis.set(self.package_name, response.content)
            redis.expire(self.package_name, settings.REDIS_EXPIRE)
            self.package_data = json2package(response.content)

        return self.package_data

    def get_implementations(self):
        """
        Get supported Python Implementations.

        :type: str or tuple of str
        """
        cs = self.package_data.python_implementations
        cs = [c.lower() for c in cs]

        if not len(cs) > 0:
            # Assume CPython
            cs = "cpython"

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

