# -*- coding: utf-8 -*-
"""
Badge.Service
=============

Talking to outside world.
Lot's of API (HTTP) requests to services, smoke their data.
Give them to :class:`painter.Draw` and let him to take care of the rest.
"""
from service import pypi


generators = {
    'pypi': {
        'd': pypi.DownloadHandler,
        'download': pypi.DownloadHandler,
        'v': pypi.VersionHandler,
        'version': pypi.VersionHandler,
        'wheel': pypi.WheelHandler,
        'egg': pypi.EggHandler,
        'license': pypi.LicenseHandler,
        'format': pypi.FormatHandler,
        'py_versions': pypi.PythonVersionsHandler,
        'implementation': pypi.ImplementationHandler,
        'status': pypi.StatusHandler,
    }
}
