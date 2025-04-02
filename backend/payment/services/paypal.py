"""Paypal services."""

import requests
from requests.auth import HTTPBasicAuth
from typing import Optional, Dict, Any, Callable

from django.conf import settings
from django.contrib.auth import get_user_model

from core.services import Amount
from ..models import PaymentStatus
from ..selectors import payment_get
from .common import external_payment_create, external_payment_capture


User = get_user_model()
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"


def paypal_payment_create(
    *,
    payer: User,
    amount: str,
    currency: str = "USD",
    return_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Create Paypal payment and commit to database."""
    payment_response = _payment_create(
        amount, currency, return_url, cancel_url
    )

    external_payment_create(
        payer=payer,
        amount=amount,
        gateway_payment_id=payment_response.get("id"),
    )

    return payment_response


def paypal_payment_capture(
    *,
    payment_id: str,
    capture_payment_func: Callable[[User, Amount], Any],
) -> Dict[str, Any]:
    """Capture Paypal payment and commit to database."""
    payment_response = _payment_capture(payment_id)

    external_payment = payment_get(gateway_payment_id=payment_id)

    if external_payment:
        external_payment_capture(
            payment=external_payment,
            capture_payment_func=capture_payment_func,
        )

    else:
        raise ValueError("Payment not found for the given payment ID.")

    return payment_response


def paypal_payment_cancel(payment_id: str) -> None:
    """Mark a PayPal payment as canceled."""
    payment = payment_get(gateway_payment_id=payment_id)
    payment.status = PaymentStatus.CANCELED
    payment.full_clean()
    payment.save()


def paypal_payout_create(
    *,
    user: User,
    amount: Amount,
    capture_payout_func: Callable[[User, Amount], Any],
    currency: str = "USD",
    note: str = "Withdrawal",
    sender_item_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Capture Paypal payout and invoke `capture_payout_func`."""
    payout_response = _payout_create(
        recipient_email=user.email,
        amount=amount,
        currency=currency,
        note=note,
        sender_item_id=sender_item_id,
    )

    capture_payout_func(user, amount)

    return payout_response


def _get_access_token() -> str:
    """Get access token for MCF."""
    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/oauth2/token",
        auth=HTTPBasicAuth(
            settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_KEY
        ),
        data={"grant_type": "client_credentials"},
    )

    response.raise_for_status()
    return response.json().get("access_token", "")


def _payment_create(
    amount: str,
    currency: str = "USD",
    return_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Create Paypal payment."""
    # https://developer.paypal.com/docs/api/orders/v2/#orders_create
    access_token = _get_access_token()
    payload: Dict[str, Any] = {
        "intent": "CAPTURE",
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "landing_page": "LOGIN",
                    "shipping_preference": "GET_FROM_FILE",
                    "user_action": "PAY_NOW",
                    "return_url": return_url or "",
                    "cancel_url": cancel_url or "",
                }
            }
        },
        "purchase_units": [
            {"amount": {"currency_code": currency, "value": amount}}
        ],
    }

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def _payment_capture(payment_id: str) -> Dict[str, Any]:
    """Capture/execute Paypal payment."""
    # https://developer.paypal.com/docs/api/orders/v2/#orders_capture
    access_token = _get_access_token()
    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders/{payment_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    response.raise_for_status()
    return response.json()


def _payout_create(
    *,
    recipient_email: str,
    amount: str,
    currency: str,
    note: str,
    sender_item_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Send money to user's PayPal email using PayPal Payouts API."""
    # https://developer.paypal.com/docs/api/payments.payouts-batch/v1/#payouts_post
    access_token = _get_access_token()

    payload = {
        "sender_batch_header": {
            "sender_batch_id": sender_item_id or "batch_" + recipient_email,
            "email_subject": "You have a payout!",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": currency,
                },
                "receiver": recipient_email,
                "note": note,
                "sender_item_id": sender_item_id or recipient_email,
            }
        ],
    }

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/payments/payouts",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=payload,
    )
    response.raise_for_status()
    return response.json()
