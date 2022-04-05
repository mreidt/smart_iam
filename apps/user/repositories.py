from typing import List

from apps.account.repositories import account_repository
from apps.user import models


class CustomUserRepository:
    model = models.CustomUser

    def get_user_by_id(self, id: int) -> models.CustomUser:
        return self.model.objects.get(id=id)

    def get_users_from_account(self, id: int):
        account = account_repository.get_account_by_id(id)
        return self.model.objects.filter(useraccount__account=account)

    def delete(self, user: models.CustomUser) -> None:
        user.delete()


class UserPermissionsRepository:
    model = models.UserPermissions

    def get_user_permissions_by_user_id(self, id: int) -> models.UserPermissions:
        user = custom_user_repository.get_user_by_id(id)
        return self.model.objects.filter(user=user, is_active=True, is_deleted=False)


class UserAccountsRepository:
    model = models.UserAccount

    def get_user_account_by_user_id(self, id: int) -> models.UserAccount:
        user = custom_user_repository.get_user_by_id(id)
        return self.model.objects.filter(user=user).first()

    def get_user_accounts_by_user_id(self, id: int) -> List[models.UserAccount]:
        user = custom_user_repository.get_user_by_id(id)
        return self.model.objects.filter(user=user)

    def get_user_account_by_id(self, id: int) -> models.UserAccount:
        return self.model.objects.get(id=id)

    def create_user_account(self, user, account):
        user_account = self.model(user=user, account=account)
        user_account.save()
        return user_account

    def delete(self, user_account: models.UserAccount) -> None:
        user_account.delete()


custom_user_repository = CustomUserRepository()
user_permission_repository = UserPermissionsRepository()
user_account_repository = UserAccountsRepository()
