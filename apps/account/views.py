from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from apps.account.models import AccountProducts, IAMAccount
from apps.account.repositories import account_repository
from apps.account.serializers import (
    AccountProductsCreateSerializer,
    AccountProductsSerializer,
    IAMAccountSerializer,
)
from apps.core.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    queryset = IAMAccount.objects.filter(is_active=True)
    serializer_class = IAMAccountSerializer
    lookup_field = "id"

    def update(self, request: Request, id: int, partial: bool = False) -> Response:
        account = account_repository.get_account_by_id(id=id)
        return super().update(request, account, partial)

    def retrieve(self, request: Request, id: int) -> Response:
        account = account_repository.get_account_by_id(id=id)
        return super().retrieve(request, account)

    def destroy(self, request: Request, id: int) -> Response:
        account = account_repository.get_account_by_id(id=id)
        return super().destroy(request, account)


class AccountProductsViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    queryset = AccountProducts.objects.all()
    serializer_class = AccountProductsSerializer
    lookup_field = "id"

    def create(self, request):
        serializer = AccountProductsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def retrieve(self, request: Request, id: int) -> Response:
        account_product = AccountProducts.objects.get(id=id)
        return super().retrieve(request, account_product)

    def update(self, request: Request, partial: bool = False) -> Response:
        account_product = AccountProducts.objects.get(id=id)
        return super().update(request, account_product, partial)

    def destroy(self, request: Request, id) -> Response:
        account_product = AccountProducts.objects.get(id=id)
        return super().destroy(request, account_product)
