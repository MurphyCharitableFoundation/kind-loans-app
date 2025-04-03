"""Contribution Views Test."""

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from loan.models import Contribution, LoanProfile
from core.services import to_money


User = get_user_model()


class ContributionViewTests(APITestCase):
    def setUp(self):
        self.lender = User.objects.create_user(
            email="lender@example.com",
            password="pass",
            amount_available=to_money(200.00),
        )
        self.borrower = User.objects.create_user(
            email="borrower@example.com", password="pass"
        )

        self.loan_profile = LoanProfile.objects.create(
            user=self.borrower,
            title="Education Loan",
            description="Help students with tuition",
            story="I need support for my studies",
            target_amount=to_money(200.00),
        )
        self.contribution = Contribution.objects.create(
            lender=self.lender,
            borrower=self.loan_profile,
            amount=150.00,
        )

    def test_contribution_list(self):
        url = reverse("contribution:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["amount"], "150.00")

    def test_contribution_detail(self):
        url = reverse("contribution:detail", args=[self.contribution.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.contribution.id)
        self.assertEqual(response.data["amount"], "150.00")

    def test_contribution_create(self):
        url = reverse("contribution:create")
        data = {
            "lender": self.lender.id,
            "borrower": self.loan_profile.id,
            "amount": "50.00",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "50.00")
        self.assertEqual(Contribution.objects.count(), 2)

    def test_contribution_history_with_lender_and_borrower_filter(self):
        url = reverse("contribution:history")
        response = self.client.get(
            url,
            {"lender": self.lender.id, "borrower": self.loan_profile.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["amount"], "150.00")
        self.assertEqual(response.data[0]["lender"], self.lender.id)
        self.assertEqual(response.data[0]["borrower"], self.loan_profile.id)
