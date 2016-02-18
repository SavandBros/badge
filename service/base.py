# -*- coding: utf-8 -*-
import logging
from painter import settings as painter_settings
from painter.draw import Draw

class ServiceBase(object):
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
        raise NotImplementedError

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
