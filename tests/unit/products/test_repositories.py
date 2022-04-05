from django.test import TestCase

from apps.products.models import Products
from apps.products.repositories import products_repository


class TestProductsRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(name="product1")

    def test_get_product_by_name(self):
        self.assertEqual(
            self.product, products_repository.get_product_by_name("product1")
        )

    def test_get_product_by_id(self):
        self.assertEqual(
            self.product, products_repository.get_product_by_id(self.product.id)
        )

    def test_delete_product(self):
        products_repository.delete(self.product)
        self.assertEqual(0, Products.objects.count())
