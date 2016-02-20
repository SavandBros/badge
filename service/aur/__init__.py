# -*- coding: utf-8 -*-
from painter import settings as painter_settings
from service.base import ServiceBase


class AURService(ServiceBase):
    def pull_package_data(self):
        pass

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
