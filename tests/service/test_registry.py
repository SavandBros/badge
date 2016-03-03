# -*- coding: utf-8 -*-
from unittest import TestCase

from service import Registry
from service.base import ServiceBase


class TestRegistry(TestCase):
    class CatService(ServiceBase):
        def action_miow(self):
            pass

        def action_piow(self):
            pass

        def action_die(self):
            pass

    def setUp(self):
        self.registry_service = Registry()
        self.registry_service.services = {}

    def test_register_service(self):
        self.registry_service.register_service(self.CatService)

        self.assertEqual(len(self.registry_service.services), 1)
        self.assertIn('cat', self.registry_service.services.keys())

    def test_purify_service_class_name(self):
        self.assertEqual(self.registry_service.purify_service_class_name(self.CatService), 'cat')

    def test_get_service_actions(self):
        self.registry_service.register_service(self.CatService)
        service_actions = self.registry_service.get_service_actions(self.CatService)

        self.assertIsInstance(service_actions, dict)
        self.assertEqual(len(service_actions), 2)

        self.assertIn('actions', service_actions)
        self.assertIn('all', service_actions)

        for action in service_actions['all']:
            self.assertNotIn('action', action)
            self.assertIn(action[0], service_actions['all'])

    def test_is_service_registry_exists(self):
        self.registry_service.register_service(self.CatService)

        self.assertTrue(self.registry_service.is_service_registry_exists('cat'))

        with self.assertRaises(LookupError):
            self.assertTrue(self.registry_service.is_service_registry_exists('dog'))

    def test_get_registry_by_class(self):
        self.registry_service.register_service(self.CatService)
        service_reg = self.registry_service.get_registry_by_class(self.CatService)

        self.assertIsNotNone(service_reg)
        self.assertEqual(service_reg, self.registry_service.services['cat'])

        with self.assertRaises(LookupError):
            self.registry_service.get_registry_by_class(object)

    def test_get_service_class_by_name(self):
        self.registry_service.register_service(self.CatService)
        service_class = self.registry_service.get_service_class_by_name('cat')

        self.assertEqual(service_class, self.CatService)

        with self.assertRaises(LookupError):
            self.registry_service.get_service_class_by_name('dog')

