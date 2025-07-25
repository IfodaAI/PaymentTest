from django.shortcuts import render
from .serializers import OrderSerializer
from .models import Order
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
