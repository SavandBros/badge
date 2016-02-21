# -*- coding: utf-8 -*-
import json

import requests

from basement import settings
from basement.settings import redis
from painter import settings as painter_settings
from service.base import ServiceBase


class AURService(ServiceBase):
    """
    AUR Service Integration
    """
    def pull_package_data(self):
        """
        :rtype: dict
        """
        pkg_url = settings.AUR_URL.format(self.package_name)
        r_data = redis.get(self.package_name)

        if r_data:
            self.package_data = json.loads(r_data)['results'][0]

        response = requests.get(pkg_url)

        if 400 <= response.status_code < 500 or 500 <= response.status_code < 600:
            self.set_package_pulling_failed()
        else:
            redis.set(self.package_name, response.content)
            redis.expire(self.package_name, settings.REDIS_EXPIRE)
            self.package_data = json.loads(response.content)['results'][0]

        return self.package_data

    def action_version(self):
        """
        Action AUR version
        """
        self.set_badge_context('version', self.package_data.get('Version'))

    def action_num_votes(self):
        """
        Action AUR NumVotes
        Showing number of votes
        """
        self.set_badge_context('votes', self.package_data.get('NumVotes'))

    def action_popularity(self):
        """
        Action AUR Popularity
        """
        self.set_badge_context('popularity', self.package_data.get('Popularity'))

    def action_status(self):
        """
        Action AUR Status
        """
        self.badge_color = painter_settings.COLOR_BRIGHT_GREEN
        badge_value = 'stable'

        pkg_status = self.package_data.get('OutOfDate', None)

        if pkg_status not in ['', None]:
            self.badge_color = painter_settings.COLOR_RED
            badge_value = 'out dated'

        self.set_badge_context('status', badge_value)

    def action_maintainer(self):
        """
        Action AUR Maintainer
        """
        self.set_badge_context(
            'maintainer',
            self.package_data.get('Maintainer')
        )

    def action_license(self):
        """
        Action AUR License
        """
        self.set_badge_context(
            'license',
            self.package_data.get('License')[0]
        )
