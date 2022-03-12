from django.test import TestCase
from rest_framework.exceptions import PermissionDenied

from apps.permissions.handlers import permissions_handler
from apps.permissions.models import Permissions
from apps.products.models import Products


class TestPermissionsHandlerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(name="product1")
        cls.permission = Permissions.objects.create(
            name="test_permission", product=cls.product
        )

    def test_delete_active_permission(self):
        with self.assertRaises(PermissionDenied):
            permissions_handler.delete_permission(self.permission.id)
        permissions = Permissions.objects.all()
        self.assertEqual(len(permissions), 1)

    def test_delete_inactive_permission(self):
        self.permission.is_active = False
        self.permission.save()
        permissions_handler.delete_permission(self.permission.id)
        self.assertFalse(Permissions.objects.exists())
