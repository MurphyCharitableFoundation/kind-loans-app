"""Loan Views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import LoanProfile
from .serializers import LoanProfileSerializer


class LoanProfileViewSet(viewsets.ModelViewSet):
    """API endpoint that allows LoanProfiles to be viewed or edited."""

    queryset = LoanProfile.objects.all()
    serializer_class = LoanProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Assign the authenticated user as the profile owner when
        creating a loan profile."""
        serializer.save(user=self.request.user)
        # TODO: Consider that the authenticated user might not be the
        # owner of the account they are updating ... their are admins
        # that help the borrowers.
