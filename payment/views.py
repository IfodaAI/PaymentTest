# views.py
from paytechuz.integrations.django.views import BasePaymeWebhookView, BaseClickWebhookView
from order.models import Order

class PaymeWebhookView(BasePaymeWebhookView):
    def before_check_perform_transaction(self, params, account):
        return {'allow': True,
                "items":[
                    {
                        "discount": 0,
                        "title": "ENTOSORAN 50 gr",
                        "price": 1500 * 100,
                        "count": 1,
                        "code": "03808001001000000",
                        "vat_percent": 12,
                        "package_code": "1470979"
                    }
                ]}

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