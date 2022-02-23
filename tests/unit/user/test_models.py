from django.test import TestCase

from apps.account.models import IAMAccount
from apps.permissions.models import Permissions
from apps.products.models import Products
from apps.user.models import CustomUser, UserAccount, UserPermissions


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="teste@email.com", password="test1234"
        )
        cls.account = IAMAccount.objects.create(email="accountemail@email.com")
        cls.product = Products.objects.create(name="product1")
        cls.permission = Permissions.objects.create(
            name="test_permission", product=cls.product
        )

    def test_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            "superuser@email.com", "superuser123"
        )
        self.assertEqual(superuser.email, "superuser@email.com")
        self.assertTrue(superuser.is_superuser)

    def test_create_user_account(self):
        user_account = UserAccount.objects.create(user=self.user, account=self.account)
        self.assertEqual(self.user, user_account.user)
        self.assertEqual(self.account, user_account.account)

    def test_create_user_permission(self):
        user_permission = UserPermissions.objects.create(
            user=self.user, permission=self.permission
        )
        self.assertEqual(self.user, user_permission.user)
        self.assertEqual(self.permission, user_permission.permission)
