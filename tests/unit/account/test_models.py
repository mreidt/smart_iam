from django.db.backends.sqlite3.base import IntegrityError
from django.test import TestCase

from apps.account.models import AccountProducts, IAMAccount
from apps.products.models import Products


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = IAMAccount.objects.create(email="accountemail@email.com")
        cls.product = Products.objects.create(name="product1")

    def test_str(self):
        self.assertEqual(str(self.account), self.account.email)

    def test_create_account(self):
        account = IAMAccount.objects.create(email="newaccount@email.com")
        self.assertEqual(account.email, "newaccount@email.com")

    def test_create_account_products(self):
        account_product = AccountProducts.objects.create(
            account=self.account, product=self.product
        )
        self.assertEqual(self.product, account_product.product)
        self.assertEqual(self.account, account_product.account)

    def test_create_account_ensure_unique_constrinat_product(self):
        AccountProducts.objects.create(account=self.account, product=self.product)

        with self.assertRaises(IntegrityError):
            AccountProducts.objects.create(account=self.account, product=self.product)
