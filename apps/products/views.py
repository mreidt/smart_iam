from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.products.handlers import products_handler
from apps.products.models import Products
from apps.products.repositories import products_repository
from apps.products.serializers import ProductCreateSerializer, ProductSerializer


class ProductViewSet(GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = Products.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = "id"

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def update(self, request, id, partial=False):
        product = products_repository.get_product_by_id(id=id)
        serializer = self.serializer_class(
            instance=product,
            data={**request.data},
            partial=partial,
        )
        if serializer.is_valid():
            updated_product = serializer.save()
            return Response(data=self.serializer_class(updated_product).data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def partial_update(self, request, id):
        return self.update(request, id, partial=True)

    def destroy(self, request, id):
        products_handler.delete_product(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
