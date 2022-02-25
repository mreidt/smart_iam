from rest_framework import serializers

from apps.products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the products object"""

    name = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Products
        fields = ["id", "name", "is_active", "created_at", "last_modified"]
        read_only_fields = ["id", "created_at", "last_modified"]


class ProductCreateSerializer(ProductSerializer):
    """Serializer for create products"""

    def create(self, validated_data):
        """Create a new product with encrypted password and return it"""
        return Products.objects.create(**validated_data)
