from django.shortcuts import render
from .serializers import OrderSerializer
from .models import Order
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from paytechuz.gateways.payme import PaymeGateway
from paytechuz.gateways.click import ClickGateway
# Create your views here.

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=(permissions.AllowAny,)

    def payme_gen(self,data):
        payme = PaymeGateway(
            payme_id="6881b7acd5ee42a97c8b6eff",
            payme_key="HJX&ESmd&ZJbZgGjuYii0uXMePcuuoHSVBN?",
            is_test_mode=False
            )
        return payme.create_payment(
            id=data['id'],
            amount=data['amount'],
            return_url="https://webapp.ifoda-shop.uz"
        )
    
    def click_gen(self,data):
        click = ClickGateway(
            service_id="79480",
            merchant_id="30842",
            merchant_user_id="61355",
            secret_key="KbcSKFP7TDVe",
            is_test_mode=False
        )
        return click.create_payment(
            id=data['id'],
            amount=data['amount'],
            return_url="https://webapp.ifoda-shop.uz",
        )

    def create(self, request, *args, **kwargs):
        payment_type=request.data.pop('payment_type')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if payment_type == 'payme':
            payment_link=self.payme_gen(serializer.data)
        else:
            payment_link=self.click_gen(serializer.data)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        data['payment_link']=payment_link
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

"""

# Buyurtmani olish
order = Order.objects.get(id=1)

# Payme to'lov havolasini yaratish
payme = PaymeGateway(
    payme_id='your_payme_id',
    payme_key='your_payme_key',
    is_test_mode=True  # Ishlab chiqarishda False qiling
)
payme_link = payme.create_payment(
    id=order.id,
    amount=order.amount,
    return_url="https://example.com/return"
)

# Click to'lov havolasini yaratish
click = ClickGateway(
    service_id='your_click_service_id',
    merchant_id='your_click_merchant_id',
    merchant_user_id='your_click_merchant_user_id',
    secret_key='your_click_secret_key',
    is_test_mode=True   # Ishlab chiqarishda False qiling
)

click_link = click.create_payment(
    id=order.id,
    amount=order.amount,
    return_url="https://example.com/return",
)

"""