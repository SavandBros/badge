# -*- coding: utf-8 -*-
from unittest import TestCase

from yarg import json2package

from basement.utils import get_file_path_from_base
from painter import settings
from service import PyPiService


class TestPyPiService(TestCase):
    package_name = "html2text"
    pypi = PyPiService(package_name)
    pypi.package_data = json2package(open(
        get_file_path_from_base('tests/service/dump_data/pypi_html2text.json')
    ).read())

    def setUp(self):
        self.pypi.badge_color = PyPiService.badge_color

    def test_get_implementations(self):
        implementations = self.pypi.get_implementations()

        self.assertEqual(implementations, 'cpython')

    def test_get_status(self):
        status = self.pypi.get_status()

        self.assertIsNotNone(status)
        self.assertIsInstance(status, list)
        self.assertEqual(len(status), 2)
        self.assertEqual(status, ['5', 'Production/Stable'])

    def test_get_license(self):
        lie_sense = self.pypi.get_license()

        self.assertEqual(lie_sense, 'GNU GPL 3')

    def test_get_versions(self):
        versions = self.pypi.get_versions()

        self.assertEqual(versions, [u'2.4', u'2.5', u'2.6', u'2.7',
                                    u'3.0', u'3.1', u'3.2', u'3.3', u'3.4'])

    def test_action_version(self):
        self.pypi.action_version()

        self.assertEqual(self.pypi.badge_key, 'version')
        self.assertIsNotNone(self.pypi.badge_value)
        self.assertIsInstance(self.pypi.badge_value, basestring)
        self.assertIn('2016', self.pypi.badge_value)

    def test_action_py_versions(self):
        self.pypi.action_py_versions()

        self.assertEqual(self.pypi.badge_color, settings.COLOR_BLUE)
        self.assertEqual(self.pypi.badge_key, 'python')

    def test_action_wheel(self):
        self.pypi.action_wheel()

        self.assertEqual(self.pypi.badge_key, 'wheel')
        self.assertEqual(self.pypi.badge_value, 'no')
        self.assertEqual(self.pypi.badge_color, settings.COLOR_RED)

    def test_action_egg(self):
        self.pypi.action_egg()

        self.assertEqual(self.pypi.badge_key, 'egg')
        self.assertEqual(self.pypi.badge_value, 'no')
        self.assertEqual(self.pypi.badge_color, settings.COLOR_BRIGHT_GREEN)

    def test_action_implementation(self):
        self.pypi.action_implementation()

        self.assertEqual(self.pypi.badge_key, 'implementation')
        self.assertEqual(self.pypi.badge_value, 'cpython')
        self.assertEqual(self.pypi.badge_color, settings.COLOR_BLUE)

