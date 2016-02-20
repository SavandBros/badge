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
