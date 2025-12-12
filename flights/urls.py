from rest_framework.routers import DefaultRouter

from flights.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet,
)

router = DefaultRouter()
router.register("types", AirplaneTypeViewSet)
router.register("list-airplanes", AirplaneViewSet)
router.register("list-crew", CrewViewSet)
router.register("list-flights", FlightViewSet)

urlpatterns = router.urls

app_name = "flights"