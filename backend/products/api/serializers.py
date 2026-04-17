from rest_framework import serializers
from products.models import Product, Category, ProductImage, ProductReview

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    vendor_name = serializers.CharField(source='vendor.store_name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'vendor_name', 'category', 'name', 'description', 'price', 'stock_quantity', 'sku', 'images', 'average_rating', 'created_at', 'updated_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']
