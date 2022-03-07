from django.db import models

from apps.products.models import Products


class Permissions(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Permissions"

    def __str__(self) -> str:
        return f"{self.name}/{self.product.name}"
