from rest_framework import serializers
from vendors.models import VendorProfile, StoreExtensionRequest
from products.models import Product, Category, ProductImage
from products.api.serializers import CategorySerializer, ProductImageSerializer
from orders.models import OrderItem


class VendorProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = VendorProfile
        fields = [
            'id',
            'store_name',
            'description',
            'logo',
            'banner',
            'brand_colors',
            'is_approved',
            'commission_rate',
            'email',
        ]
        read_only_fields = ['is_approved']


class StoreExtensionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreExtensionRequest
        fields = ['id', 'vendor', 'reason', 'status', 'created_at']
        read_only_fields = ['vendor', 'status']


class VendorProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image_file = serializers.ImageField(write_only=True, required=False, allow_null=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_id',
            'images',
            'image_file',
            'name',
            'description',
            'price',
            'stock_quantity',
            'sku',
            'average_rating',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        product = super().create(validated_data)
        if image_file:
            ProductImage.objects.create(product=product, image=image_file, is_primary=True)
        return product


class VendorOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    tracking_number = serializers.CharField(source='order.tracking_number', read_only=True)
    customer_email = serializers.CharField(source='order.user.email', read_only=True)
    vendor_earnings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    commission_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'tracking_number',
            'customer_email',
            'product',
            'product_name',
            'quantity',
            'price_at_purchase',
            'commission_amount',
            'vendor_earnings',
            'status',
        ]
        read_only_fields = [
            'product',
            'quantity',
            'price_at_purchase',
            'commission_amount',
            'vendor_earnings',
        ]
