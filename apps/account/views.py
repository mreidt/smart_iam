from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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


class AccountProductsViewSet(GenericViewSet):
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
        serializer = self.serializer_class(account_product)
        return Response(data=serializer.data)

    def destroy(self, request: Request, id: int) -> Response:
        account_product = AccountProducts.objects.get(id=id)
        account_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request: Request) -> Response:
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
