from django.db import models
from django.conf import settings

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendors/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='vendors/banners/', blank=True, null=True)
    brand_colors = models.JSONField(blank=True, null=True, help_text='Store custom brand colors as JSON')
    is_approved = models.BooleanField(default=False)
    auto_renewal = models.BooleanField(default=True, help_text='For subscription billing auto renewal')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text='Platform commission rate in percentage')

    def __str__(self):
        return self.store_name

class StoreExtensionRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='extension_requests')
    reason = models.TextField(help_text="Why do you need a store extension?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Extension Request - {self.vendor.store_name} ({self.status})"
