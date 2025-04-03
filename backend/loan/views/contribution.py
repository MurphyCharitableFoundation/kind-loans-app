"""Loan Views."""

from django.http import Http404

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Contribution
from ..services import contribution_create
from ..selectors import contribution_get, contribution_list


class ContributionListAPI(APIView):
    """Contribution List API."""

    class OutputSerializer(serializers.ModelSerializer):
        """Contributions Output Serializer."""

        class Meta:
            model = Contribution
            fields = ("id", "lender", "borrower", "amount", "created")

    def get(self, request):
        """GET Contributions."""
        contributions = contribution_list()

        data = self.OutputSerializer(contributions, many=True).data

        return Response(data)


class ContributionDetailAPI(APIView):
    """Contribution Detail API."""

    class OutputSerializer(serializers.ModelSerializer):
        """Contribution Output Serializer."""

        class Meta:
            model = Contribution
            fields = ("id", "lender", "borrower", "amount", "created")

    def get(self, request, contribution_id):
        """GET Contribution."""
        contribution = contribution_get(contribution_id)

        if not contribution:
            raise Http404

        data = self.OutputSerializer(contribution).data

        return Response(data)


class ContributionCreateAPI(APIView):
    """Contribution Create API."""

    class InputSerializer(serializers.ModelSerializer):
        """Contribution Input Serializer."""

        class Meta:
            model = Contribution
            fields = ("id", "lender", "borrower", "amount")

    def post(self, request):
        """POST Contribution."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contribution = contribution_create(**serializer.validated_data)

        data = ContributionDetailAPI.OutputSerializer(contribution).data

        return Response(data)


class ContributionHistoryAPI(APIView):
    """
    Contribution History API.

    Filter contribution history by lender and loan profile.
    """

    def get(self, request):
        """GET history."""
        lender_id = request.GET.get("lender")
        borrower_id = request.GET.get("borrower")

        filters = {}
        if lender_id:
            filters["lender"] = lender_id
        if borrower_id:
            filters["borrower"] = borrower_id

        contributions = contribution_list(filters=filters)
        data = ContributionListAPI.OutputSerializer(
            contributions, many=True
        ).data
        return Response(data)
