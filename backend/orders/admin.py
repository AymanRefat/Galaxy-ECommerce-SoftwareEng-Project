from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Transaction
from vendors.admin_mixins import VendorModelAdminMixin

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__email', 'session_id')

    def has_module_permission(self, request): return request.user.is_superuser
    def has_add_permission(self, request): return request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    search_fields = ('tracking_number', 'user__email', 'user__username')
    readonly_fields = ('created_at',)

    def has_module_permission(self, request): return request.user.is_superuser
    def has_add_permission(self, request): return request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser

@admin.register(OrderItem)
class OrderItemAdmin(VendorModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'vendor', 'quantity', 'price_at_purchase', 'status')
    list_filter = ('status',)
    search_fields = ('order__tracking_number', 'product__name', 'vendor__store_name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'order__tracking_number')

    def has_module_permission(self, request): return request.user.is_superuser
    def has_add_permission(self, request): return request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser
