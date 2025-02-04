from transaction.models import ExternalPayment
from transaction.utils import configure_paypal
from paypalrestsdk import Payment, Payout

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from datetime import datetime


def create_paypal_transaction(payer, amount, return_url, cancel_url):
    """Create a real-money transaction with PayPal"""
    configure_paypal()

    payment_data = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [
            {
                "amount": {
                    "total": f"{amount.amount:.2f}",
                    "currency": amount.currency.code,
                },
                "description": "Payment transaction description",
            }
        ],
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
    }
    payment = Payment(payment_data)

    if payment.create():
        ExternalPayment.objects.create(
            gateway_payment_id=payment.id,
            amount=amount,
            user=payer,
        )
        return payment, None
    else:
        raise Exception(payment.error)


def execute_paypal_transaction(payment_id, payer_id, payment_func):
    """Execute a real-money transaction with PayPal"""
    configure_paypal()

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        try:
            external_payment = ExternalPayment.objects.get(
                gateway_payment_id=payment_id
            )
            external_payment.transaction = payment_func(
                external_payment.user, external_payment.amount
            )
            external_payment.status = "COMPLETED"
            external_payment.save()

            return payment
        except ObjectDoesNotExist:
            raise ValueError("Transaction not found for the given payment ID.")
    else:
        raise Exception(payment.error)


def execute_paypal_payout_transaction(payee, amount, payout_func):
    """Execute a real-money payout transaction to email"""
    configure_paypal()

    payout = Payout(
        {
            "sender_batch_header": {
                "sender_batch_id": f"user_{payee.id}_time_{datetime.now()}",
                "email_subject": f"Payment from {settings.MCF_APP_NAME}",
                "email_message": "Thanks for using our service!",
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": f"{amount.amount:.2f}",
                        "currency": amount.currency.code,
                    },
                    "receiver": payee.email,
                    "note": "Thanks for your patronage!",
                    "sender_item_id": "item_000",
                }
            ],
        }
    )

    if payout.create(sync_mode=False):
        # sync_mode=False for delayed/async confirmation
        print("Payout created successfully")
        print("Payout ID:", payout.batch_header.payout_batch_id)
        payout_func(payee, amount)
    else:
        raise Exception(payout.error)
