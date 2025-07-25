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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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