import paypalrestsdk

from .models import User, LoanProfile
from .utils import configure_paypal
from payment.models import Transaction, TransactionStatus


class PayPalPaymentHandler:
    def __init__(self):
        configure_paypal()

    def create_payment(
        self, payer_id, recipient_id, amount, return_url, cancel_url
    ):
        # Define the payment request
        payment = paypalrestsdk.Payment(
            {
                # TODO: better nomer for intent, description
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {
                            "total": f"{amount:.2f}",
                            "currency": "USD",
                        },
                        "description": "Payment transaction description",
                    }
                ],
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url,
                },
            }
        )

        # Attempt to create the payment
        if payment.create():
            # If payment creation is successful,
            # create a corresponding Transaction
            lender = User.objects.get(id=payer_id)
            borrower = LoanProfile.objects.get(id=recipient_id)

            transaction = Transaction.objects.create_transaction(
                amount=amount,
                payer=lender,
                recipient=borrower,
                payment_id=payment.id,
            )
            return payment, transaction
        else:
            # Handle the error if creation failed
            raise Exception(payment.error)

    def execute_payment(self, payment_id, payer_id):
        # Execute the payment after PayPal approval
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Update the transaction status
            transaction = Transaction.objects.get(payment_id=payment_id)
            transaction.status = TransactionStatus.COMPLETED
            transaction.save()

            return payment
        else:
            raise Exception(payment.error)
