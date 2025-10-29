from django.db import models
from categories.models import Category
# Create your models here.



class Service(models.Model):
    icon = models.ImageField(upload_to='service_icons/', blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in hours")
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0, null=True, blank=True)
    availability = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    

