from rest_framework.routers import DefaultRouter

from airports.views import AirportViewSet, RouteViewSet

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = router.urls

app_name = "airports"
