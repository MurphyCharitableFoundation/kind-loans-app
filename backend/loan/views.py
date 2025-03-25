"""Loan Views."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import LoanProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import LoanProfileSerializer


class LoanProfileViewSet(viewsets.ModelViewSet):
    """API endpoint that allows LoanProfiles to be viewed or edited."""

    queryset = LoanProfile.objects.all()
    serializer_class = LoanProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Assign the authenticated user as the profile owner when
        creating a loan profile."""
        serializer.save(user=self.request.user)
        # TODO: Consider that the authenticated user might not be the
        # owner of the account they are updating ... their are admins
        # that help the borrowers.

    @action(detail=True, methods=["get"])
    def story(self, request, pk=None):
        """Return only story a specific LoanProfile."""
        loan_profile = self.get_object()
        return Response({"story": loan_profile.story})
