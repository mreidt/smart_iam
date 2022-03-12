from rest_framework import routers

from apps.account.views import AccountProductsViewSet, AccountViewSet

app_name = "account"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"account", AccountViewSet, basename="account")
router.register(
    r"account-products", AccountProductsViewSet, basename="account-products"
)

urlpatterns = router.urls
