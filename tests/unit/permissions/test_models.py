from django.test import TestCase

from apps.permissions.models import Permissions
from apps.products.models import Products


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(name="product1")
        cls.permission = Permissions.objects.create(
            name="test_permission", product=cls.product
        )

    def test_str(self):
        self.assertEqual(
            str(self.permission),
            f"{self.permission.name}/{self.permission.product.name}",
        )

    def test_create_permission(self):
        permission = Permissions.objects.create(
            name="new_permission", product=self.product
        )
        self.assertEqual("new_permission", permission.name)
        self.assertEqual(self.product, permission.product)
