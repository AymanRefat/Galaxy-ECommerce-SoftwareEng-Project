from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview
from vendors.admin_mixins import VendorModelAdminMixin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Product)
class ProductAdmin(VendorModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'stock_quantity', 'sku', 'created_at')
    list_filter = ('category', 'created_at', 'vendor')
    search_fields = ('name', 'sku', 'description', 'vendor__store_name')
    inlines = [ProductImageInline, ProductReviewInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'vendor_profile'):
            return qs.filter(product__vendor=request.user.vendor_profile)
        return qs.none()

    def has_module_permission(self, request):
        return request.user.is_superuser  # Hide from index for vendors
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
