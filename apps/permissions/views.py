from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.permissions.models import Permissions
from apps.permissions.serializers import (
    PermissionsCreateSerializer,
    PermissionsSerializer,
)
from apps.permissions.repositories import permissions_repository
from apps.permissions.handlers import permissions_handler


class PermissionsViewSet(GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = Permissions.objects.filter(is_active=True)
    serializer_class = PermissionsSerializer
    looku_field = "id"

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PermissionsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def update(self, request, id: int, partial: bool=False):
        permission = permissions_repository.get_permission_by_id(id=id)
        serializer = self.serializer_class(instance=permission, data={**request.data}, partial=partial)
        if serializer.is_valid():
            updated_permission = serializer.save()
            return Response(data=self.serializer_class(updated_permission).data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def partial_update(self, request, id: int):
        return self.update(request, id, partial=True)
    
    def destroy(self, request, id: int):
        permissions_handler.delete_permission(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
