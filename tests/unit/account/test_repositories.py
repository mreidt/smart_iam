from django.test import TestCase

from apps.account.models import AccountProducts, IAMAccount
from apps.account.repositories import account_products_repository, account_repository
from apps.products.models import Products


class TestAccountRepositories(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = IAMAccount.objects.create(email="accountemail@email.com")

    def test_get_account_by_id(self):
        self.assertEqual(
            account_repository.get_account_by_id(self.account.id), self.account
        )


class TestAccountProductsRepositories(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = IAMAccount.objects.create(email="accountemail@email.com")
        cls.product = Products.objects.create(name="product1")
        cls.account_product = AccountProducts.objects.create(
            account=cls.account, product=cls.product
        )

    def test_get_account_products(self):
        account_products = account_products_repository.get_account_products(
            self.account.id
        )
        self.assertEqual(len(account_products), 1)
        self.assertEqual(account_products[0], self.account_product)
