from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    category = serializers.CharField(source='service.category.name', read_only=True)
    customer_first_name = serializers.CharField(source='customer.user.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.user.last_name', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'service', 'customer', 'created_at')