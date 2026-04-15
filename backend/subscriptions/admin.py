from django.contrib import admin
from .models import SubscriptionPlan, VendorSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(VendorSubscription)
