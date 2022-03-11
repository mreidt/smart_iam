from rest_framework import routers

from apps.permissions.views import PermissionsViewSet

app_name = "permissions"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"permissions", PermissionsViewSet, basename="permissions")

urlpatterns = router.urls
