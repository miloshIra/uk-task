from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import resources

router = DefaultRouter()
router.register(r"battle", resources.BattleViewSet)

urlpatterns = [
    path("check/", resources.health_check, name="health_check"),
    path(
        "battle/<str:pokemon1>/<str:pokemon2>/",
        resources.BattleViewSet.as_view({"post": "create"}),
    ),
    path("", include(router.urls)),
]
