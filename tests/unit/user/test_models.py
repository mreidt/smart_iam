from django.test import TestCase

from apps.user.models import CustomUser


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser(email="teste@email.com", password="test1234")

    def test_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            "superuser@email.com", "superuser123"
        )
        self.assertEqual(superuser.email, "superuser@email.com")
        self.assertTrue(superuser.is_superuser)
