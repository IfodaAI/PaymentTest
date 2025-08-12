# views.py
from paytechuz.integrations.django.views import BasePaymeWebhookView, BaseClickWebhookView
from order.models import Order

class PaymeWebhookView(BasePaymeWebhookView):
    def check_transaction(self, params, transaction):
        """
        Called when checking a transaction.

        Args:
            params: Request parameters
            transaction: Transaction object
        """
        # This method is meant to be overridden by subclasses
        return {
            'transaction': transaction.transaction_id,
            'state': transaction.state,
            'create_time': int(transaction.created_at.timestamp() * 1000),
            'perform_time': (
                int(transaction.performed_at.timestamp() * 1000)
                if transaction.performed_at else 0
            ),
            'cancel_time': (
                int(transaction.cancelled_at.timestamp() * 1000)
                if transaction.cancelled_at else 0
            ),
            "detail":{
                "receipt_type": 0,
                "items":[
                    {
                        "discount": 0,
                        "title": "Доставка",
                        "price": 1500 * 100,
                        "count": 1,
                        "code": "10112006002000000",
                        "vat_percent": 12,
                        "package_code": "1542432"
                    }
                ]
            },
            'reason': transaction.reason,
        }

    def successfully_payment(self, params, transaction):
        order = Order.objects.get(id=transaction.account_id)
        order.status = 'paid'
        order.save()
        print(f"Order {order.id} paid — params: {params}, txn_id: {transaction.id}", flush=True)

    def cancelled_payment(self, params, transaction):
        order = Order.objects.get(id=transaction.account_id)
        order.status = 'cancelled'
        order.save()
        print(f"Order {order.id} cancelled — params: {params}, txn_id: {transaction.id}", flush=True)

class ClickWebhookView(BaseClickWebhookView):
    def successfully_payment(self, params, transaction):
        order = Order.objects.get(id=transaction.account_id)
        order.status = 'paid'
        order.save()

    def cancelled_payment(self, params, transaction):
        order = Order.objects.get(id=transaction.account_id)
        order.status = 'cancelled'
        order.save()