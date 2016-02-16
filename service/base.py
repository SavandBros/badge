# -*- coding: utf-8 -*-
class ServiceBase(object):
    badge_key = None
    badge_value = None
    format = 'svg'
    cash_it = False

    def prepare_badge_context(self, package_data):
        """
        Basically handle the incoming data from service which hosts the
        package or project.

        The data must be provided in :class:`dict` class and parsing the data,
        like converting from another type such as JSON should be handled
        before reaching to this method.

        Required context:

            * badge_key: The Subject of the badge.
            * badge_value: The message of the badge.

        :param package_data: A dictionary of package's data retrieved from
        service that hosts the package.
        :type: dict

        :returns: A dictionary of required info for making the badge.
        :rtype: dict
        """
        raise NotImplementedError

