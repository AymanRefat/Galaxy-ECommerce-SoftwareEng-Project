import pytest
from rest_framework.test import APIClient
from users.models import User
from vendors.models import VendorProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestUserAPI:
    def test_register_consumer(self, api_client):
        url = '/api/users/register/'
        data = {
            'email': 'consumer_test@example.com',
            'username': 'consumer_test',
            'password': 'StrongPassword123!',
            'user_type': 'CONSUMER'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='consumer_test@example.com').exists()
        assert not hasattr(User.objects.get(email='consumer_test@example.com'), 'vendor_profile')

    def test_register_vendor(self, api_client):
        url = '/api/users/register/'
        data = {
            'email': 'vendor_test@example.com',
            'username': 'vendor_test',
            'password': 'StrongPassword123!',
            'user_type': 'VENDOR',
            'store_name': 'My Super Store'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        user = User.objects.get(email='vendor_test@example.com')
        assert hasattr(user, 'vendor_profile')
        assert user.vendor_profile.store_name == 'My Super Store'
        assert not user.vendor_profile.is_approved

    def test_login(self, api_client):
        User.objects.create_user(username='loginuser', email='login@example.com', password='password123')
        url = '/api/users/login/'
        response = api_client.post(url, {'email': 'login@example.com', 'password': 'password123'})
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
