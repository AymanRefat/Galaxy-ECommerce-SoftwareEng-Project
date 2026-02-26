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

    def __str__(self):
        return self.store_name
