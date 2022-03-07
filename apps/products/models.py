from django.db import models


class Products(models.Model):
    name = models.CharField(unique=True, max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name
