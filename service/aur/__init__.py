# -*- coding: utf-8 -*-

from painter import settings as painter_settings
from service.base import ServiceBase


class AURService(ServiceBase):
    """
    AUR Service Integration
    """
    service_url = 'https://aur.archlinux.org//rpc/?v=5&type=info&arg[]={0}'

    def clean_validate_package_data(self, package_data):
        """
        :type package_data: dict
        :rtype: dict
        """
        if package_data['resultcount'] == 0:
            return False

        package_data = package_data['results'][0]

        return {
            'Version': package_data.get('Version'),
            'NumVotes': package_data.get('NumVotes', 0),
            'Popularity': package_data.get('Popularity'),
            'OutOfDate': package_data.get('OutOfDate', None),
            'License': package_data.get('License'),
            'Maintainer': package_data.get('Maintainer'),
        }

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
        self.set_badge_context('votes', str(self.package_data.get('NumVotes', 0)))

    def action_popularity(self):
        """
        Action AUR Popularity
        """
        self.set_badge_context('popularity', str(self.package_data.get('Popularity')))

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
        self.badge_color = painter_settings.COLOR_BLUE
        self.set_badge_context(
            'license',
            self.package_data.get('License')[0]
        )
