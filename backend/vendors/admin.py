from django.contrib import admin
from .models import VendorProfile, StoreExtensionRequest
from .admin_mixins import VendorModelAdminMixin

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_approved', 'auto_renewal')
    list_filter = ('is_approved', 'auto_renewal')
    search_fields = ('store_name', 'user__email', 'user__username', 'description')
    actions = ['approve_vendors', 'disapprove_vendors']

    @admin.action(description="Approve selected vendors")
    def approve_vendors(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Disapprove selected vendors")
    def disapprove_vendors(self, request, queryset):
        queryset.update(is_approved=False)

    def has_module_permission(self, request): return request.user.is_superuser
    def has_add_permission(self, request): return request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser

@admin.register(StoreExtensionRequest)
class StoreExtensionRequestAdmin(VendorModelAdminMixin, admin.ModelAdmin):
    list_display = ('vendor', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('vendor__store_name', 'reason')
