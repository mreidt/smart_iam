from django.db import models

from apps.products.models import Products


class IAMAccount(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.email


class AccountProducts(models.Model):
    account = models.ForeignKey(IAMAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.account}/{self.product}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["account", "product"], name="unique_product_per_account"
            )
        ]
