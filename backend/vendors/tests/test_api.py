import pytest
from rest_framework.test import APIClient
from products.models import Product, Category
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

@pytest.mark.django_db
class TestVendorAPI:
    def test_list_public_vendors(self, api_client, vendor_profile):
        url = '/api/vendors/'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['store_name'] == 'Store 1'

@pytest.mark.django_db
class TestVendorDashboardAPI:
    def test_vendor_can_load_own_profile(self, api_client, vendor_user, vendor_profile):
        api_client.force_authenticate(user=vendor_user)

        response = api_client.get('/api/vendors/dashboard/profile/')

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['store_name'] == vendor_profile.store_name

    def test_approved_vendor_can_create_product(self, api_client, vendor_user, vendor_profile):
        api_client.force_authenticate(user=vendor_user)
        payload = {
            'name': 'Dashboard Product',
            'description': 'Created from the seller dashboard.',
            'price': '49.99',
            'stock_quantity': 12,
            'sku': 'DASH-001',
        }

        response = api_client.post('/api/vendors/dashboard/products/', payload, format='json')

        assert response.status_code == 201
        product = Product.objects.get(sku='DASH-001')
        assert product.vendor == vendor_profile

    def test_pending_vendor_cannot_create_product(self, api_client, vendor_user, vendor_profile):
        vendor_profile.is_approved = False
        vendor_profile.save()
        api_client.force_authenticate(user=vendor_user)

        response = api_client.post('/api/vendors/dashboard/products/', {
            'name': 'Blocked Product',
            'description': 'This should not be created.',
            'price': '19.99',
            'stock_quantity': 3,
            'sku': 'BLOCKED-001',
        }, format='json')

        assert response.status_code == 403
        assert not Product.objects.filter(sku='BLOCKED-001').exists()
