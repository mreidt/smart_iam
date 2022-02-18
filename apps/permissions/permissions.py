import logging

from rest_framework.permissions import IsAuthenticated
from apps.account.repositories import account_products_repository
from apps.user.repositories import user_permission_repository

logger = logging.getLogger(__name__)


class IsAccountAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(IsAccountAdmin, self).has_permission(request, view):
            return False
        has_permission = request.user.admin
        if not has_permission:
            logger.info(f"The user with id {request.user.id}, is not account admin.")
        return has_permission


class AccountHasProduct(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(AccountHasProduct, self).has_permission(request, view):
            return False
        
        if not hasattr(view, "products") or not view.products:
            raise AttributeError("To use this permission in your view, you should set 'products' attribute.")

        account_id = request.account.id
        account_products = set(account_products_repository.get_account_products(account_id))
        required_products = set(view.products)
        has_permission = required_products.issubset(account_products)

        if not has_permission:
            missing_products = required_products.difference(account_products)
            logger.info(f"The required products {missing_products} are missing for account {account_id}.")
        
        return has_permission


class UserHasProductPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(UserHasProductPermissions, self).has_permission(request, view):
            return False

        if not hasattr(view, "user_permissions") or not view.user_permissions:
            raise AttributeError("To use this permission in your view, you should ser 'user_permissions' attribute.")

        user_id = request.user.id
        user_permissions = set(user_permission_repository.get_user_permissions_by_id(user_id))
        required_permissions = set(view.user_permissions)
        has_permission = required_permissions.issubset(user_permissions)

        if not has_permission:
            missing_permissions = required_permissions.difference(user_permissions)
            logger.info(f"The required permissions {missing_permissions} are missing for user {user_id}.")
        
        return has_permission
