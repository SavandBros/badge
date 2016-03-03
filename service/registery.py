# -*- coding: utf-8 -*-
from service.base import ServiceBase


class Registry(object):
    services = {}

    def register_service(self, service_class):
        """
        :param service_class: The services module.
        :type service_class: ServiceBase

        :rtype: ServiceBase
        """
        if not issubclass(service_class, ServiceBase):
            raise TypeError('"{}" is not a subclass of "ServiceBase"'.format(
                service_class.__name__))

        service_actions = self.get_service_actions(service_class)

        self.services.update({
            self.purify_service_class_name(service_class): {
                'class': service_class,
                'actions': {
                    'actions': service_actions['actions'],
                    'all': service_actions['all'],
                }
            }
        })

    @staticmethod
    def purify_service_class_name(service_class):
        """
        :type service_class: ServiceBase

        :rtype: str
        """
        return service_class.__name__.split('Service')[0].lower()

    @staticmethod
    def get_service_actions(service_class):
        """
        :param service_class: The services module.
        :type service_class: ServiceBase

        :rtype: dict of dict
        """
        service_vars = service_class.__dict__
        actions = {}
        all_actions = {}

        for k in service_vars.keys():
            if k.startswith('action_'):
                action_name = k.split('action_')[1]
                action_short_name = action_name[0]
                actions[action_name] = {
                    'full_name': k,
                    'short_name': action_short_name,
                    'display_name': action_name.capitalize(),
                }
                all_actions.update({
                    action_name: k,
                    action_short_name: k,
                })

        return {
            'actions': actions,
            'all': all_actions,
        }

    def is_service_registry_exists(self, service_name):
        """
        :type service_name: str

        :raises: LookupError if it doesn't exists.
        :rtype: bool
        """
        if service_name not in self.services:
            raise LookupError('"{}" is not registered'.format(service_name))

        return True

    def get_registry_by_class(self, service_class):
        """
        :type service_name: str

        :rtype: dict of str and ServiceBase
        """
        service_name = self.purify_service_class_name(service_class)
        self.is_service_registry_exists(service_name)

        return self.services[service_name]

    def get_service_class_by_name(self, service_name):
        """
        :type service_name: str

        :rtype: ServiceBase or class
        """
        self.is_service_registry_exists(service_name)

        return self.services[service_name]['class']
