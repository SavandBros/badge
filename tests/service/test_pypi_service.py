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

