import logging

from rest_framework.permissions import IsAuthenticated

from apps.account.repositories import account_products_repository
from apps.products.repositories import products_repository
from apps.user.repositories import user_account_repository, user_permission_repository

logger = logging.getLogger(__name__)


class IsAccountAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(IsAccountAdmin, self).has_permission(request, view):
            return False
        user = request.user
        user_account = user_account_repository.get_user_account_by_user_id(user.id)
        if not user_account:
            logger.info(
                f"The user with id {request.user.id}, does not have an account."
            )
            return False
        has_permission = user_account.admin
        if not has_permission:
            logger.info(f"The user with id {request.user.id}, is not account admin.")
        return has_permission


class AccountHasProduct(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(AccountHasProduct, self).has_permission(request, view):
            return False

        if not hasattr(view, "products") or not view.products:
            raise AttributeError(
                "To use this permission in your view, you should set 'products' attribute."
            )

        user = request.user
        user_account = user_account_repository.get_user_account_by_user_id(user.id)
        account_id = user_account.account.id

        account_products = set(
            [
                account_product.product
                for account_product in account_products_repository.get_account_products(
                    account_id
                )
            ]
        )
        required_products = set(
            [
                products_repository.get_product_by_name(product)
                for product in view.products
            ]
        )
        has_permission = required_products.issubset(account_products)

        if not has_permission:
            missing_products = required_products.difference(account_products)
            logger.info(
                f"The required products {missing_products} are missing for account {account_id}."
            )

        return has_permission


class UserHasPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(UserHasPermissions, self).has_permission(request, view):
            return False

        if not hasattr(view, "user_permissions") or not view.user_permissions:
            raise AttributeError(
                "To use this permission in your view, you should set 'user_permissions' attribute."
            )

        user_id = request.user.id
        user_account = user_account_repository.get_user_account_by_user_id(user_id)
        if not user_account:
            logger.info(
                f"The user with id {request.user.id}, does not have an account."
            )
            return False
        if user_account.admin:
            return True
        user_permissions = set(
            user_permission_repository.get_user_permissions_by_user_id(user_id)
        )
        required_permissions = set(view.user_permissions)
        has_permission = required_permissions.issubset(user_permissions)

        if not has_permission:
            missing_permissions = required_permissions.difference(user_permissions)
            logger.info(
                f"The required permissions {missing_permissions} are missing for user {user_id}."
            )

        return has_permission
