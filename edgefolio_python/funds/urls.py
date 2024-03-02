from rest_framework import routers
from .views import FundViewSet
from django.urls import include, path

app_name = "funds"
router = routers.DefaultRouter()
router.register(r"funds", FundViewSet, basename="fund")

urlpatterns = [
    path("", include(router.urls)),
]
