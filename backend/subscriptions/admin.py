from django.contrib import admin
from .models import SubscriptionPlan, VendorSubscription
from vendors.admin_mixins import VendorModelAdminMixin

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_price')
    search_fields = ('name',)

    def has_module_permission(self, request): return request.user.is_superuser
    def has_add_permission(self, request): return request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser

@admin.register(VendorSubscription)
class VendorSubscriptionAdmin(VendorModelAdminMixin, admin.ModelAdmin):
    list_display = ('vendor', 'plan', 'status', 'start_date', 'end_date', 'paid_price')
    list_filter = ('status', 'plan', 'start_date', 'end_date')
    search_fields = ('vendor__store_name', 'plan__name')
    readonly_fields = ('start_date', 'end_date')
