# -*- coding: utf-8 -*-
import unittest
import sys

from fabfile import grintify
from fabfile import env


@grintify
def run_tests():
    """
    Running tests
    """
    tests = unittest.TestLoader().discover(env.root)
    runner = unittest.TextTestRunner()
    results = runner.run(tests)
    sys.exit(not results.wasSuccessful())
