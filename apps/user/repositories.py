from apps.user import models


class CustomUserRepository:
    model = models.CustomUser

    def get_user_by_uuid(self, uuid):
        return self.model.objects.get(uuid=uuid)

    def get_user_by_id(self, id):
        return self.model.objects.get(id=id)


class UserPermissionsRepository:
    model = models.UserPermissions

    def get_user_permissions_by_uuid(self, uuid):
        user = custom_user_repository.get_user_by_uuid(uuid)
        return self.model.objects.filter(user=user, is_active=True, is_deleted=False)

    def get_user_permissions_by_id(self, id):
        user = custom_user_repository.get_user_by_id(id)
        return self.model.objects.filter(user=user, is_active=True, is_deleted=False)


custom_user_repository = CustomUserRepository()
user_permission_repository = UserPermissionsRepository()
