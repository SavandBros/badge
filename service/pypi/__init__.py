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
        """
        Get status of package on PyPi.
        """
        if (not isinstance(self.package_data.classifiers, list) and
            not len(self.package_data.classifiers) > 0 ):
            return "none found"

        for classifier in self.package_data.classifiers:
            if classifier.startswith("Development Status"):
                bits = classifier.split(' :: ')
                return bits[1].split(' - ')

        return "1", "unknown"

    def get_license(self):
        """
        Get the package license from PyPi.

        :rtype: str
        """
        if (self.package_data.license
            and '\n' not in self.package_data.license
            and self.package_data.license.upper() != 'UNKNOWN'):
            return self.package_data.license

        if self.package_data.license_from_classifiers:
            return self.package_data.license_from_classifiers

        return "unknown"

    def action_version(self):
        """
        Action PyPi Package version
        """
        self.set_badge_context(
            'version',
            self.package_data.latest_release_id.replace('-', '--')
        )

    def action_wheel(self):
        """
        Action PyPi Wheel
        """
        has_wheel = self.package_data.has_wheel
        self.badge_color = (painter_settings.COLOR_BRIGHT_GREEN
                            if has_wheel else painter_settings.COLOR_RED)
        self.set_badge_context(
            "wheel",
            "yes" if has_wheel else "no"
        )

    def action_egg(self):
        """
        Action PyPi Egg
        """

        has_egg = self.package_data.has_egg
        self.badge_color = (painter_settings.COLOR_RED
                            if has_egg else painter_settings.COLOR_BRIGHT_GREEN)
        self.set_badge_context(
            "egg",
            "yes" if has_egg else "no"
        )

    def action_implementation(self):
        """
        Action PyPi Implementation
        """
        versions = self.get_implementations()
        self.badge_color = painter_settings.COLOR_BLUE

        if isinstance(versions, list):
            versions = ", ".join(versions)

        self.set_badge_context("implementation", versions)

    def action_status(self):
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
        self.badge_color = statuses[code]
        status = status.lower().replace('-', '--')
        status = "stable" if status == "production/stable" else status

        self.set_badge_context("status", status)
