# -*- coding: utf-8 -*-
import logging
from painter import settings as painter_settings
from painter.draw import Draw

class ServiceBase(object):
    badge_key = None
    badge_value = None
    format = 'svg'
    cash_it = False

    def pull_package_data(self):
        """
        Pulling package data from hosting service that keeps the packages.

        The data must be returned in :class:`dict`.
        Any information about the package that the other `actions` of the
        service needs should be returned.

        The data of the package will be cached and will be used later by
        the actions,

        :returns: A dictionary of required info for making the badge.
        :rtype: dict
        """
        raise NotImplementedError

