import pytest
from rest_framework.test import APIClient
from products.models import Product, Category
from vendors.models import VendorProfile
from users.models import User
from orders.models import Cart, CartItem, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def consumer_user():
    user = User.objects.create_user(username='consumer1', email='consumer1@example.com', password='password', user_type='CONSUMER')
    return user

@pytest.fixture
def vendor_user():
    user = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='password', user_type='VENDOR')
    return user

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name='Store 1', is_approved=True)

@pytest.fixture
def product(vendor_profile):
    category = Category.objects.create(name='Electronics', slug='electronics')
    return Product.objects.create(
        vendor=vendor_profile,
        category=category,
        name='Phone',
        description='A smartphone',
        price='100.00',
        stock_quantity=10,
        sku='PHONE-001'
    )

@pytest.mark.django_db
class TestOrderAPI:
    def test_add_to_cart_anonymous(self, api_client, product):
        url = '/api/cart/add_item/'
        # Add item to cart
        response = api_client.post(url, {'product': product.id, 'quantity': 2}, format='json')
        assert response.status_code == 201
        
        # Check cart
        response = api_client.get('/api/cart/')
        assert response.status_code == 200
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['quantity'] == 2

    def test_checkout_authenticated(self, api_client, consumer_user, product):
        api_client.force_authenticate(user=consumer_user)
        # Add item to cart
        api_client.post('/api/cart/add_item/', {'product': product.id, 'quantity': 2}, format='json')
        
        # Checkout
        url = '/api/orders/checkout/'
        response = api_client.post(url, {'payment_token': 'VALID_TOKEN'}, format='json')
        assert response.status_code == 201
        assert response.data['total_amount'] == '200.00'
        assert Order.objects.count() == 1
        assert Order.objects.first().user == consumer_user
        
        # Check cart is empty
        response = api_client.get('/api/cart/')
        assert len(response.data['items']) == 0
