from apps.user import models


class CustomUserRepository:
    model = models.CustomUser

    def get_user_by_id(self, id: int) -> models.CustomUser:
        return self.model.objects.get(id=id)


class UserPermissionsRepository:
    model = models.UserPermissions

    def get_user_permissions_by_user_id(self, id: int) -> models.UserPermissions:
        user = custom_user_repository.get_user_by_id(id)
        return self.model.objects.filter(user=user, is_active=True, is_deleted=False)


custom_user_repository = CustomUserRepository()
user_permission_repository = UserPermissionsRepository()
