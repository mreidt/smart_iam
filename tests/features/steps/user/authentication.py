from behave import given
from rest_framework.authtoken.models import Token

from apps.user.models import CustomUser


@given("I have a valid user")
def given_step_valid_user(context):
    context.user = CustomUser.objects.create(email="user@email.com", password="pass123")


@given("I am a staff user")
def given_step_staff_user(context):
    context.user = CustomUser.objects.create_superuser(
        email="superuser@email.com", password="pass123"
    )


@given("I have a valid token")
def given_valid_token(context):
    context.token = Token.objects.get_or_create(user=context.user)[0].key
