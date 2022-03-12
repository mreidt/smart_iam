from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(GenericViewSet):
    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def list(self, request: Request) -> Response:
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def update(self, request: Request, instance, partial: bool = False) -> Response:
        serializer = self.serializer_class(
            instance=instance, data={**request.data}, partial=partial
        )
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(data=self.serializer_class(updated_instance).data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def partial_update(self, request: Request, id: int):
        return self.update(request, id, partial=True)

    def retrieve(self, request: Request, instance) -> Response:
        serializer = self.serializer_class(instance)
        return Response(data=serializer.data)

    def destroy(self, request: Request, instance) -> Response:
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
