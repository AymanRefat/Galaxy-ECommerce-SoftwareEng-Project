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

# TestVendorDashboardAPI was removed because dashboard was migrated to Django Admin
