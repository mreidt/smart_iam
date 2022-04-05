import logging

from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.views import BaseViewSet
from apps.permissions.permissions import (
    AccountHasProduct,
    IsAccountAdmin,
    UserHasPermissions,
)
from apps.user.handlers import custom_user_handler
from apps.user.models import CustomUser
from apps.user.repositories import custom_user_repository, user_account_repository
from apps.user.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(BaseViewSet):
    permission_classes = [IsAccountAdmin, UserHasPermissions, AccountHasProduct]
    lookup_field = "id"
    user_permissions = ["smart_iam/list_users"]
    products = ["smart_iam"]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def list(self, request):
        user_account = user_account_repository.get_user_account_by_user_id(
            id=request.user.id
        )
        serializer = self.serializer_class(
            custom_user_repository.get_users_from_account(user_account.account.id),
            many=True,
        )
        return Response(serializer.data)

    def create(self, request):
        user_account = user_account_repository.get_user_account_by_user_id(
            id=request.user.id
        )
        serializer = UserSerializer(data={**request.data})

        if serializer.is_valid():
            try:
                with (transaction.atomic()):
                    user = serializer.save()
                    user_account_repository.create_user_account(
                        user, user_account.account
                    )
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            except Exception as ex:
                logger.exception(
                    f"During user creation, following exception was raised: {ex}"
                )
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=ex)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def update(self, request: Request, id: int, partial: bool = False) -> Response:
        user = custom_user_repository.get_user_by_id(id=id)
        return super().update(request, user, partial)

    def retrieve(self, request: Request, id: int) -> Response:
        user = custom_user_repository.get_user_by_id(id=id)
        return super().retrieve(request, user)

    def destroy(self, request: Request, id: int) -> Response:
        custom_user_handler.delete_user(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
