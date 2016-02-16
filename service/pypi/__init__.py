# -*- coding: utf-8 -*-
"""
PyPi
====

Everything around PyPi
"""

import hashlib

import requests
from yarg.package import json2package

from basement.settings import redis
from basement.utils import intword_converters, escape_shield_query
from basement import settings
from painter import settings as painter_settings
from painter.draw import Draw


class PypiHandler(object):
    '''Get the pypi json data for the package, and process.'''
    shield_subject = None
    request = None
    format = 'svg'
    cacheable = False

    def get(self, request, package, format, *args, **kwargs):
        self.request = request
        self.format = format
        url = settings.PYPI_URL % package
        r_data = redis.get(package)
        if r_data:
            self.package = json2package(r_data)
            return self.handle_package_data()
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.shield_subject = 'error'
            return self.write_shield('error', painter_settings.COLOR_RED)
        else:
            redis.set(package, response.content)
            redis.expire(package, settings.REDIS_EXPIRE)
            self.package = json2package(response.content)
            return self.handle_package_data()

    def handle_package_data(self):
        '''Look at the pypi data and decide what text goes on the badge.'''
        raise NotImplementedError

    def hash(self, url):
        return hashlib.md5(url).hexdigest()

    def write_shield(self, status, colour=painter_settings.COLOR_GREEN):
        '''Obtain and write the shield to the response.'''
        # shield_url = settings.SHIELD_URL % (
        #     self.shield_subject,
        #     status,
        #     colour,
        #     self.format,
        # )
        # style = self.request.args.get('style', 'flat')
        # if style is not None and style[0] in ['flat', 'flat-square', 'plastic' ]:
        #     style = style[0]
        # shield_url += "?style={0}".format(style)
        # shield_url = shield_url.replace(" ", "_")
        # 
        # ihash = self.hash(shield_url)
        # cache = os.path.join(settings.FILE_CACHE, ihash)
        # if os.path.exists(cache) and self.cacheable:
        #     mtime = os.stat(cache).st_mtime + settings.CACHE_TIME
        #     if mtime > time.time():
        #         return open(cache).read()
        # 
        # shield_response = requests.get(shield_url, stream=True)
        # img = BytesIO()
        # for chunk in shield_response.iter_content(1024):
        #     if not chunk:
        #         break
        #     img.write(chunk)
        # if self.cacheable:
        #     with open(cache, 'w') as ifile:
        #         img.seek(0)
        #         ifile.write(img.read())
        # img.seek(0)
        # return img.read()
        draw = Draw(self.shield_subject, colour, status)

        return draw.as_svg() if self.format == 'svg' else draw.as_png()


class DownloadHandler(PypiHandler):
    shield_subject = 'downloads'

    # Pretty much taken straight from Django
    def intword(self, value):
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

    def handle_package_data(self):
        period = self.request.args.get('period', 'month')
        if isinstance(period, list):
            period = period[0]
        if period not in ('day', 'week', 'month'):
            period = 'month'
        downloads = getattr(self.package.downloads, period)
        downloads = self.intword(downloads)
        pperiod = "%s/%s" % (downloads, period)
        return self.write_shield(pperiod)


class VersionHandler(PypiHandler):
    shield_subject = 'pypi'

    def handle_package_data(self):
        text = self.request.args.get('text', 'pypi')
        if text[0] in ('pypi', 'version'):
            self.shield_subject = text[0]
        return self.write_shield(self.package.latest_release_id.replace('-', '--'))


class WheelHandler(PypiHandler):
    shield_subject = 'wheel'
    cacheable = True

    def handle_package_data(self):
        has_wheel = self.package.has_wheel
        wheel_text = "yes" if has_wheel else "no"
        colour = painter_settings.COLOR_BRIGHT_GREEN if has_wheel else painter_settings.COLOR_RED
        return self.write_shield(wheel_text, colour)


class EggHandler(PypiHandler):
    shield_subject = 'egg'
    cacheable = True

    def handle_package_data(self,):
        has_egg = self.package.has_egg
        egg_text = "yes" if has_egg else "no"
        colour = painter_settings.COLOR_RED if has_egg else painter_settings.COLOR_BRIGHT_GREEN
        return self.write_shield(egg_text, colour)


class FormatHandler(PypiHandler):
    shield_subject = 'format'
    cacheable = True

    def handle_package_data(self):
        has_egg = self.package.has_egg
        colour = painter_settings.COLOR_YELLOW
        text = "source"
        text = "egg" if has_egg else text
        colour = painter_settings.COLOR_RED if has_egg else colour
        has_wheel = self.package.has_wheel
        text = "wheel" if has_wheel else text
        colour = painter_settings.COLOR_BRIGHT_GREEN if has_wheel else colour
        return self.write_shield(text, colour)


class LicenseHandler(PypiHandler):
    shield_subject = 'license'
    cacheable = True

    def get_license(self):
        '''Get the package license.'''
        if self.package.license and '\n' not in self.package.license and \
        self.package.license.upper() != 'UNKNOWN':
            return self.package.license
        if self.package.license_from_classifiers:
            return self.package.license_from_classifiers
        return "unknown"

    def handle_package_data(self):
        license = self.get_license()
        license = escape_shield_query(license)
        colour = (painter_settings.COLOR_BLUE 
                  if license != "unknown" else painter_settings.COLOR_RED)
        return self.write_shield(license, colour)


class PythonVersionsHandler(PypiHandler):
    shield_subject = 'python'
    cacheable = True

    def get_versions(self):
        """"
        Get supported Python versions
        """
        if not isinstance(self.package.classifiers, list) and \
        not len(self.package.classifiers) > 0:
            return "none found"
        cs = self.package.python_versions
        cs = sorted(set(cs))
        if not len(cs) > 0:
            # assume 2.7
            return "2.7"
        return cs

    def handle_package_data(self):
        versions = self.get_versions()
        if not isinstance(versions, list):
            return self.write_shield(versions, 'blue')
        return self.write_shield(", ".join(versions), 'blue')


class ImplementationHandler(PypiHandler):
    shield_subject = 'implementation'
    cacheable = True

    def get_implementations(self):
        """"
        Get supported Python implementations
        """
        cs = self.package.python_implementations
        cs = [c.lower() for c in cs]
        if not len(cs) > 0:
            # assume CPython
            return 'cpython'
        return cs

    def handle_package_data(self):
        versions = self.get_implementations()
        if not isinstance(versions, list):
            return self.write_shield(versions, 'blue')
        return self.write_shield(", ".join(versions), 'blue')


class StatusHandler(PypiHandler):
    shield_subject = 'status'
    cacheable = True

    def get_status(self):
        if not isinstance(self.package.classifiers, list) and \
        not len(self.package.classifiers) > 0:
            return "none found"
        for classifier in self.package.classifiers:
            if classifier.startswith("Development Status"):
                bits = classifier.split(' :: ')
                return bits[1].split(' - ')
        return "1", "unknown"

    def handle_package_data(self):
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
        return self.write_shield(status, statuses[code])
