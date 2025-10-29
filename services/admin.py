from django.contrib import admin
from .models import Service
# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'duration', 'price')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('name', 'category')