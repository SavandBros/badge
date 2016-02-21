# -*- coding: utf-8 -*-
"""
Badge.Service
=============

Talking to outside world.
Lot's of API (HTTP) requests to services, smoke their data.
Give them to :class:`painter.Draw` and let him to take care of the rest.
"""
from service.aur import AURService
from service.registery import Registry
from service.pypi import PyPiService

service_registry = Registry()
service_registry.register_service(PyPiService)
service_registry.register_service(AURService)
