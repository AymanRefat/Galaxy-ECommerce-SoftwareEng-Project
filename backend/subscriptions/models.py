from django.db import models 
from vendors.models import VendorProfile

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(blank=True, null=True, help_text="List of features included")

    def __str__(self):
        return self.name

class VendorSubscription(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('PAST_DUE', 'Past Due'),
    )
    vendor = models.OneToOneField(VendorProfile, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    paid_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price paid at subscription time")

    def __str__(self):
        return f"{self.vendor.store_name} - {self.plan.name if self.plan else 'Unknown Plan'}"
