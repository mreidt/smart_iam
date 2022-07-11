from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from apps.account.models import AccountProducts, IAMAccount
from apps.products.models import Products
from apps.products.serializers import ProductSerializer


class IAMAccountSerializer(serializers.ModelSerializer):
    """Serializer for the IAMAccount object"""

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=IAMAccount.objects.all())]
    )
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = IAMAccount
        fields = [
            "id",
            "email",
            "is_active",
            "is_deleted",
            "created_at",
            "last_modified",
        ]
        read_only_fields = ["id", "created_at", "last_modified"]


class AccountProductsSerializer(serializers.ModelSerializer):
    """Serializer for the AccountProducts object"""

    account = IAMAccountSerializer()
    product = ProductSerializer()

    class Meta:
        model = AccountProducts
        fields = [
            "id",
            "account",
            "product",
            "is_active",
            "is_deleted",
            "created_at",
            "last_modified",
        ]
        read_only_fields = ["id", "created_at", "last_modified"]


class AccountProductsCreateSerializer(serializers.ModelSerializer):
    """Serializer for create the AccountProducts object"""

    account = serializers.SlugRelatedField(
        slug_field="id", queryset=IAMAccount.objects.all()
    )
    product = serializers.SlugRelatedField(
        slug_field="id", queryset=Products.objects.all()
    )

    class Meta:
        model = AccountProducts
        fields = [
            "id",
            "account",
            "product",
            "is_active",
            "is_deleted",
            "created_at",
            "last_modified",
        ]
        read_only_fields = ["id", "created_at", "last_modified"]
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("account", "product"),
                message="This account already has this product.",
            )
        ]
