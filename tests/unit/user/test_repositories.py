from django.test import TestCase

from apps.permissions.models import Permissions
from apps.products.models import Products
from apps.user.models import CustomUser, UserPermissions
from apps.user.repositories import custom_user_repository, user_permission_repository


class TestCustomUserRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="teste@email.com", password="test1234"
        )

    def test_get_user_by_id(self):
        self.assertEqual(self.user, custom_user_repository.get_user_by_id(self.user.id))


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
