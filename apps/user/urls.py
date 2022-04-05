from rest_framework import routers

from apps.user.views import UserViewSet

app_name = "user"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
