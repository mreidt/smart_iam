from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urls = [
    path("", include("apps.products.urls")),
    path("", include("apps.permissions.urls")),
]

urlpatterns = [
    path("smart-iam/api/admin/", admin.site.urls),
    path("smart-iam/api/", include(urls)),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
