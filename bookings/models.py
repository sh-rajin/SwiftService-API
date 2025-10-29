from django.db import models
from services.models import Service
from customer.models import Customer
# Create your models here.

class Booking(models.Model):
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Service'),
        ('pay_now', 'Pay Now'),
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200, help_text="Enter Address....")
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS, default='pending', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Service : {self.service.name} - Customer : {self.customer.user.first_name}"
