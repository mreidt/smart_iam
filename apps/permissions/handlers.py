from rest_framework.exceptions import PermissionDenied

from apps.permissions.repositories import permissions_repository


class PermissionsHandlers(object):
    def delete_permission(self, permission_id: int) -> None:
        permission = permissions_repository.get_permission_by_id(permission_id)

        if permission.is_active:
            raise PermissionDenied("Cannot delete active permission.")

        permissions_repository.delete(permission)


permissions_handler = PermissionsHandlers()
