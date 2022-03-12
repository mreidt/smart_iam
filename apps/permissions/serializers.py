from rest_framework import serializers

from apps.permissions.models import Permissions


class PermissionsSerializer(serializers.ModelSerializer):
    """Serializer for the permissions object"""

    name = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Permissions
        fields = [
            "id",
            "name",
            "product",
            "description",
            "is_active",
            "is_deleted",
            "created_at",
            "last_modified",
        ]
        read_only_fields = ["id", "created_at", "last_modified"]


class PermissionsCreateSerializer(PermissionsSerializer):
    """Serializer for create permissions"""

    def create(self, validated_data):
        """Create a new product with encrypted password and return it"""
        return Permissions.objects.create(**validated_data)
