from rest_framework import serializers
from .models import Review
from services.serializers import ServiceSerializer


class ReviewSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    customer_first_name = serializers.CharField(source='customer.user.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.user.last_name', read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'customer', 'service')