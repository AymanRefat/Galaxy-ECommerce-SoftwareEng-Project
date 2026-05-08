import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from products.models import Product, Category
from products.api.views import DEFAULT_CATEGORIES
from vendors.models import VendorProfile
from users.models import User
from orders.models import Order, OrderItem

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def vendor_user():
    user = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='password', user_type='VENDOR')
    return user

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name='Store 1', is_approved=True)

@pytest.fixture
def category():
    return Category.objects.create(name='Electronics', slug='electronics')

@pytest.fixture
def product(vendor_profile, category):
    return Product.objects.create(
        vendor=vendor_profile,
        category=category,
        name='Phone',
        description='A smartphone',
        price='999.99',
        stock_quantity=10,
        sku='PHONE-001'
    )

@pytest.mark.django_db
class TestProductAPI:
    def test_list_products(self, api_client, product):
        url = '/api/products/'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Phone'

    def test_list_categories(self, api_client, category):
        url = '/api/categories/'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == len(DEFAULT_CATEGORIES)

        category_slugs = {item['slug'] for item in response.data}
        assert category.slug in category_slugs
        assert {slug for slug, _ in DEFAULT_CATEGORIES} == category_slugs

    def test_search_products(self, api_client, product):
        url = '/api/products/?search=smartphone'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_filter_products(self, api_client, product, category):
        url = f'/api/products/?category__slug={category.slug}'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

@pytest.fixture
def consumer_user():
    return User.objects.create_user(username='consumer', email='consumer@test.com', password='password')

@pytest.fixture
def purchased_product(consumer_user, product):
    order = Order.objects.create(user=consumer_user, tracking_number='TRK-123', total_amount=999.99)
    OrderItem.objects.create(order=order, product=product, vendor=product.vendor, quantity=1, price_at_purchase=999.99)
    return product

@pytest.mark.django_db
class TestProductReviewAPI:
    def test_review_without_purchase(self, api_client, consumer_user, product):
        api_client.force_authenticate(user=consumer_user)
        response = api_client.post('/api/reviews/', {'product': product.id, 'rating': 5, 'comment': 'Great!'})
        assert response.status_code == 403

    def test_review_with_purchase(self, api_client, consumer_user, purchased_product):
        api_client.force_authenticate(user=consumer_user)
        response = api_client.post('/api/reviews/', {'product': purchased_product.id, 'rating': 5, 'comment': 'Great!'})
        assert response.status_code == 201
