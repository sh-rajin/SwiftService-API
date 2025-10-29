from django.contrib import admin
from .models import Booking
# Register your models here.
@admin.register(Booking)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'customer', 'created_at')
    