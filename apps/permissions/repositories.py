from apps.permissions import models


class PermissionsRepository:
    model = models.Permissions

    def get_permission_by_id(self, id: int) -> models.Permissions:
        return self.model.objects.get(id=id)
    def delete(self, permission: models.Permissions) -> None:
        permission.delete()


permissions_repository = PermissionsRepository()
