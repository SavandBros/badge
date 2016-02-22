# -*- coding: utf-8 -*-
"""
PyPi
====

Everything around PyPi
"""

from yarg.package import json2package

from basement.utils import escape_shield_query, intword
from painter import settings as painter_settings
from service.base import ServiceBase


class PyPiService(ServiceBase):
    """
    PyPi Service integration
    """
    service_url = "https://pypi.python.org/pypi/{0}/json"

    def package_data_parser(self):
        """
        :rtype: method
        """
        return json2package

    def clean_validate_package_data(self, package_data):
        """
        :type package_data: dict
        :rtype: dict
        """
        # TODO: Return only what's needed
        return package_data

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

    def get_versions(self):
        """
        Get supported python versions
        """
        if (not isinstance(self.package_data.classifiers, list) and
            not len(self.package_data.classifiers) > 0):
            return "none found"

        cs = self.package_data.python_versions
        cs = sorted(set(cs))

        if not len(cs) > 0:
            # Assume "2.7
            return "2.7"

        return cs

    def action_version(self):
        """
        Action PyPi Package version
        """
        self.set_badge_context(
            'version',
            self.package_data.latest_release_id.replace('-', '--')
        )

    def action_py_versions(self):
        """
        Action PyPi Python Versions
        """
        versions = self.get_versions()
        self.badge_color = painter_settings.COLOR_BLUE

        if isinstance(versions, list):
            versions = ", ".join(versions)

        self.set_badge_context('python', versions)

    def action_wheel(self):
        """
        Action PyPi Wheel
        """
        if self.is_package_latest_release_invalid():
            self.badge_color = painter_settings.COLOR_RED
            self.set_badge_context('wheel', 'unknown')
            return

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
        if self.is_package_latest_release_invalid():
            self.badge_color = painter_settings.COLOR_RED
            self.set_badge_context('egg', 'unknown')
            return

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

    def action_license(self):
        """
        Action PyPi License
        """
        lie_sense = self.get_license()
        lie_sense = escape_shield_query(lie_sense)
        self.badge_color = (painter_settings.COLOR_BLUE
                            if lie_sense != "unknown"
                            else painter_settings.COLOR_RED)

        self.set_badge_context('license', lie_sense)

    def action_format(self):
        """
        Action PyPi Format
        """
        if self.is_package_latest_release_invalid():
            self.badge_color = painter_settings.COLOR_RED
            self.set_badge_context('format', 'unknown')
            return

        has_egg = self.package_data.has_egg
        color = painter_settings.COLOR_YELLOW
        badge_value = "source"
        badge_value = "egg" if has_egg else badge_value
        color = painter_settings.COLOR_RED if has_egg else color
        has_wheel = self.package_data.has_wheel
        badge_value = "wheel" if has_wheel else badge_value
        color = painter_settings.COLOR_BRIGHT_GREEN if has_wheel else color

        self.badge_color = color
        self.set_badge_context('format', badge_value)

    def action_downloads(self):
        """
        Action PyPi Downloads
        """
        period = self.extra_context.get('period', 'month')

        if isinstance(period, list):
            period = period[0]

        if period not in ('day', 'week', 'month'):
            period = "month"

        downloads = getattr(self.package_data.downloads, period)
        downloads = intword(downloads)

        self.set_badge_context("downloads", "{}/{}".format(downloads, period))

    def is_package_latest_release_invalid(self):
        """
        Since #https://github.com/SavandBros/badge/issues/44 it
        seems the latest_release of parsed package_data by
         :mod:``yarg.package`` has None value.

        It's a bug from yarg which I don't have much time to fix and send
        the patch to the maintainer. The original author of yarg
        package seems to be inactive recently.

        No issues, gonna handle it here.
        Basically not a thing but a good thing to be in a separate
        method.

        :rtype: bool
        """
        return self.package_data.latest_release is None
