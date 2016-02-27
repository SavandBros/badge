# -*- coding: utf-8 -*-
import logging
import json
import hashlib
import pickle

import requests

from basement import settings
from basement.settings import redis
from painter import settings as painter_settings
from painter.draw import Draw


class ServiceBase(object):
    """
    :type service_api_url: str
    :type service_url: str
    :type display_name: str
    :type badge_key: str
    :type badge_value: str
    :type badge_color: str
    :type package_name: str
    :type package_pulling_failed: bool
    :type package_pulling_failed_key: str
    :type package_pulling_failed_value: str
    :type format: str
    :type cash_it: bool
    :type extra_context: dict
    """
    service_api_url = None
    service_url = None
    display_name = None
    badge_key = None
    badge_value = None
    badge_color = painter_settings.COLOR_GREEN
    package_name = None
    package_data = {}
    package_pulling_failed = False
    package_pulling_failed_key = 'error'
    package_pulling_failed_value = 'error'
    format = 'svg'
    cash_it = True
    cash_key = None
    extra_context = {}

    def __init__(self, package_name, format=None, cash_it=True,
                 extra_context=None, *args, **kwargs):
        self.package_name = package_name
        self.format = format or self.format
        self.cash_it = cash_it
        self.extra_context = extra_context or {}

    def get_package_api_url(self):
        """
        Build package url from its service.

        :rtype: str
        """
        return self.service_api_url.format(self.package_name)

    def get_package_url(self):
        """
        Build package url, for linking usage and humans eyes.

        :rtype: str
        """
        return self.service_url.format(self.package_name)

    def get_package_raw_content(self):
        """
        Get package raw content from the service.
        The content are usually in text, no parsing should happen here and
        this is the only to fire up some HTTP request.

        :rtype: str or None
        """
        response = requests.get(self.get_package_api_url())

        if 400 <= response.status_code < 500 or 500 <= response.status_code < 600:
            self.set_package_pulling_failed()
            return None

        return response.content

    def package_data_parser(self):
        """
        Package raw content parser method.
        By default json.loads

        :rtype: method
        """
        return json.loads

    def parse_package_data(self, raw_data):
        """
        A method for parsing the raw data from API.
        The default method of parsing is JSON.

        In this method we'll be using `json` from Python Standard Library.
        Each service should implement this method.

        Should return the parsed data, if failed, `False` should be returned.

        :type raw_data: str or object

        :rtype: bool or dict
        """
        try:
            return self.package_data_parser()(raw_data)
        except ValueError as exc:
            logging.error("Error in parsing the data.\n"
                          "Traceback: {}".format(str(exc)))

            return False

    def pull_package_data(self):
        """
        Pulling package data from hosting service that keeps the packages.

        The data must be returned in :class:`dict`.
        Any information about the package that the other `actions` of the
        service needs should be returned.

        The data of the package will be cached and will be used later by
        the actions,

        :returns: A dictionary of required info for making the badge.
        :rtype: dict
        """
        cache_key = self.get_cache_key()
        package_data = redis.get(cache_key)

        if package_data:
            logging.info("Getting {0} from cache".format(self.package_name))
            self.package_data = pickle.loads(package_data)
            return self.package_data

        raw_content = self.get_package_raw_content()
        if raw_content:
            package_data = self.parse_package_data(raw_content)

        if package_data:
            package_data = self.clean_validate_package_data(package_data)

        if package_data is not False:
            if self.cash_it:
                logging.info("Caching pkg {} from service: {}".format(
                    self.package_name, self.__class__.__name__))

                redis.set(cache_key, pickle.dumps(package_data))
                redis.expire(cache_key, settings.REDIS_EXPIRE)
            self.package_data = package_data

        if not package_data:
            self.set_package_pulling_failed()
        else:
            return self.package_data

    def draw_badge(self):
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
        badge_key = self.badge_key
        badge_color = self.badge_color
        badge_value = self.badge_value

        if self.package_pulling_failed:
            badge_key = self.package_pulling_failed_key
            badge_value = self.package_pulling_failed_value
            badge_color = painter_settings.COLOR_RED

        draw = Draw(
            key_text=badge_key,
            value_color=badge_color,
            value_text=badge_value
        )

        return draw.as_svg() if self.format == 'svg' else draw.as_png()

    def set_package_pulling_failed(self, failed=True):
        """
        :param failed: Either pulling the data failed or not, that's the thing.
        :type failed: bool

        :rtype: None
        """
        logging.error('Pulling package: "{}" failed '
                      'from service: "{}"'.format(self.package_name,
                                                  self.__class__.__name__))
        self.package_pulling_failed = failed
        self.package_data = None

    def set_badge_context(self, badge_key, badge_value):
        """
        Setting badge context, first key/subject and value/status.

        :param badge_key: Badge Key/Subject
        :type badge_key: str

        :param badge_value: Badge Value/Status
        :type badge_value: str

        :rtype: None
        """
        self.badge_key = badge_key
        self.badge_value = badge_value

    def get_cache_key(self):
        """
        Create cache key from :method:`get_package_api_url`

        :rtype: str
        """
        if not self.cash_key:
            self.cash_key = hashlib.md5(self.get_package_api_url()).hexdigest()

        return self.cash_key

    def clean_validate_package_data(self, package_data):
        """
        Clean and Validate package data.

        * If the package data is broken, not complete then it should return error.
        * If the package data comes with extra stuff, then they should be
            simply removed and cleaned.
        * While cleaning, only return stuff that needed for making badge.

        :type package_data: dict

        :rtype: dict or bool
        """
        raise NotImplementedError
