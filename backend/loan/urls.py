from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoanProfileViewSet

router = DefaultRouter()
router.register(r"profile", LoanProfileViewSet, basename="loan-profile")

urlpatterns = [
    path("", include(router.urls)),
]
