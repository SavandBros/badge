# -*- coding: utf-8 -*-
from unittest import TestCase
import json

from basement.utils import get_file_path_from_base
from painter import settings
from service.aur import AURService


class TestAURService(TestCase):
    package_name = "git-cola"
    pypi = AURService(package_name)
    package_data = json.loads(open(
        get_file_path_from_base('tests/service/dump_data/aur_git-cola.json')
    ).read())['results'][0]

    def setUp(self):
        self.pypi.badge_color = AURService.badge_color
        self.pypi.package_data = self.package_data

    def test_action_version(self):
        self.pypi.action_version()

        self.assertEqual(self.pypi.badge_value, self.package_data['Version'])

    def test_action_num_votes(self):
        self.pypi.action_num_votes()

        self.assertEqual(self.pypi.badge_value, self.package_data['NumVotes'])

    def test_action_popularity(self):
        self.pypi.action_popularity()

        self.assertEqual(self.pypi.badge_value, self.package_data['Popularity'])

    def test_action_status(self):
        self.pypi.action_status()

        self.assertEqual('stable', self.pypi.badge_value)
        # FIXME: Not sure about out of date value
        self.pypi.package_data['OutOfDate'] = '2016.45.21'
        self.pypi.action_status()
        self.assertEqual(self.pypi.badge_value, 'out dated')
        self.assertEqual(self.pypi.badge_color, settings.COLOR_RED)

    def test_action_maintainer(self):
        self.pypi.action_maintainer()

        self.assertEqual(self.pypi.badge_value, self.package_data['Maintainer'])

    def test_action_license(self):
        self.pypi.action_license()

        self.assertEqual(self.pypi.badge_value, self.package_data['License'][0])

