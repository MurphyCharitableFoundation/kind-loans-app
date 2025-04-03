"""Loan urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    LoanProfileViewSet,
    ContributionListAPI,
    ContributionDetailAPI,
    ContributionCreateAPI,
)

router = DefaultRouter()
router.register(r"profile", LoanProfileViewSet, basename="loan-profile")

contribution_patterns = [
    path(
        "",
        ContributionListAPI.as_view(),
        name="list",
    ),
    path(
        "<int:contribution_id>/",
        ContributionDetailAPI.as_view(),
        name="detail",
    ),
    path("create/", ContributionCreateAPI.as_view(), name="create"),
]

urlpatterns = [
    path(
        "contribution/",
        include((contribution_patterns, "contribution")),
    ),
    path("", include(router.urls)),
]
