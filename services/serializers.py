from rest_framework import serializers
from .models import Service
from categories.serializers import CategorySerializer

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'rating', 'review_count', 'availability')

    