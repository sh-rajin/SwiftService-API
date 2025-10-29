from django.db import models
from services.models import Service
from django.contrib.auth.models import User
from customer.models import Customer
from django.core.validators import MaxValueValidator
# Create your models here.

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        service = self.service
        reviews = service.reviews.all()
        service.review_count = reviews.count()
        service.rating = sum(r.rating for r in reviews) / reviews.count()
        service.save()

    def __str__(self):
        return f'Review by {self.customer.user.username} for {self.service.name}'
