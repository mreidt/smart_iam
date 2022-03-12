from django.test import TestCase
from rest_framework.exceptions import PermissionDenied

from apps.products.handlers import products_handler
from apps.products.models import Products


class TestProductsHandlerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(name="product1")

    def test_delete_active_product(self):
        with self.assertRaises(PermissionDenied):
            products_handler.delete_product(self.product.id)
        products = Products.objects.all()
        self.assertEqual(len(products), 1)

    def test_delete_inactive_product(self):
        self.product.is_active = False
        self.product.save()
        products_handler.delete_product(self.product.id)
        self.assertFalse(Products.objects.exists())
