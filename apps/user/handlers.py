from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from apps.user.repositories import custom_user_repository, user_account_repository


class CustomUserHandlers(object):
    @transaction.atomic
    def delete_user(self, user_id: int) -> None:
        user = custom_user_repository.get_user_by_id(user_id)

        if user.is_active:
            raise PermissionDenied("Cannot delete active user.")

        user_accounts = user_account_repository.get_user_accounts_by_user_id(user_id)
        for user_account in user_accounts:
            user_account_handler.delete_user_account(user_account.id)

        custom_user_repository.delete(user)


class UserAccountHandlers(object):
    def delete_user_account(self, user_account_id: int) -> None:
        user_account = user_account_repository.get_user_account_by_id(user_account_id)
        user_account_repository.delete(user_account)


user_account_handler = UserAccountHandlers()
custom_user_handler = CustomUserHandlers()
