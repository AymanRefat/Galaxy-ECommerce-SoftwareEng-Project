from rest_framework import serializers
from vendors.models import VendorProfile, StoreExtensionRequest
from products.models import Product

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['id', 'store_name', 'description', 'logo', 'banner', 'brand_colors', 'is_approved']
        read_only_fields = ['is_approved']

class StoreExtensionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreExtensionRequest
        fields = ['id', 'vendor', 'reason', 'status', 'created_at']
        read_only_fields = ['vendor', 'status']

class VendorProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'stock_quantity', 'sku', 'created_at', 'updated_at']

from orders.models import OrderItem

class VendorOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    tracking_number = serializers.CharField(source='order.tracking_number', read_only=True)
    customer_email = serializers.CharField(source='order.user.email', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'tracking_number', 'customer_email', 'product', 'product_name', 'quantity', 'price_at_purchase', 'status']
        read_only_fields = ['product', 'quantity', 'price_at_purchase']
