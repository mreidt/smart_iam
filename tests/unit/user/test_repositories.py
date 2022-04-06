from django.test import TestCase

from apps.account.models import IAMAccount
from apps.permissions.models import Permissions
from apps.products.models import Products
from apps.user.models import CustomUser, UserAccount, UserPermissions
from apps.user.repositories import (
    custom_user_repository,
    user_account_repository,
    user_permission_repository,
)


class TestCustomUserRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="teste@email.com", password="test1234"
        )
        cls.account = IAMAccount.objects.create(email="teste@email.com")
        cls.user_account = UserAccount.objects.create(
            user=cls.user, account=cls.account
        )

    def test_get_user_by_id(self):
        self.assertEqual(self.user, custom_user_repository.get_user_by_id(self.user.id))

    def test_get_users_from_account(self):
        user_list = custom_user_repository.get_users_from_account(self.account.id)
        self.assertEqual(1, len(user_list))
        self.assertEqual(self.user, user_list[0])

    def test_delete_user(self):
        custom_user_repository.delete(self.user)
        self.assertEqual(0, CustomUser.objects.count())


class TestUserPermissionRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="teste@email.com", password="test1234"
        )
        cls.product = Products.objects.create(name="product1")
        cls.permission = Permissions.objects.create(
            name="test_permission", product=cls.product
        )
        cls.user_permission = UserPermissions.objects.create(
            user=cls.user, permission=cls.permission
        )

    def test_get_user_permissions_by_id(self):
        user_permissions = user_permission_repository.get_user_permissions_by_user_id(
            self.user.id
        )
        self.assertEqual(len(user_permissions), 1)
        self.assertEqual(self.user_permission, user_permissions[0])


class TestUserAccountsRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="teste@email.com", password="test1234"
        )
        cls.account = IAMAccount.objects.create(email="teste@email.com")
        cls.user_account = UserAccount.objects.create(
            user=cls.user, account=cls.account
        )

    def test_get_user_account_by_user_id(self):
        self.assertEqual(
            self.user_account,
            user_account_repository.get_user_account_by_user_id(self.user.id),
        )

    def test_get_user_accounts_by_user_id(self):
        user_accounts = user_account_repository.get_user_accounts_by_user_id(
            self.user.id
        )
        self.assertEqual(1, len(user_accounts))
        self.assertEqual(self.user_account, user_accounts[0])

    def test_get_user_account_by_id(self):
        self.assertEqual(
            self.user_account,
            user_account_repository.get_user_account_by_id(self.user_account.id),
        )

    def test_create_user_account(self):
        new_user_account = user_account_repository.create_user_account(
            self.user, self.account
        )
        self.assertEqual(2, UserAccount.objects.count())
        self.assertIn(new_user_account, UserAccount.objects.all())

    def test_delete_user_account(self):
        user_account_repository.delete(self.user_account)
        self.assertEqual(0, UserAccount.objects.count())
