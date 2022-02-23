from django.test import TestCase

from apps.products.models import Products


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(name="product1")

    def test_str(self):
        self.assertEqual(str(self.product), self.product.name)

    def test_create_product(self):
        product = Products.objects.create(name="product2")
        self.assertEqual("product2", product.name)
