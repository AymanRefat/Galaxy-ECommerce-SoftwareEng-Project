import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from vendors.models import VendorProfile, StoreExtensionRequest
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(email="admin@example.com", username="admin", password="password123")

@pytest.fixture
def vendor_user():
    user = User.objects.create_user(email="vendor@example.com", username="vendoruser", password="password123")
    return user

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name="Test Store", is_approved=True)

@pytest.mark.django_db
def test_request_store_extension(api_client, vendor_user, vendor_profile):
    api_client.force_authenticate(user=vendor_user)
    
    url = reverse('vendor-extension-list')
    response = api_client.post(url, {'reason': 'I need more space to sell products.'})
    
    assert response.status_code == 201
    assert StoreExtensionRequest.objects.count() == 1
    
    extension = StoreExtensionRequest.objects.first()
    assert extension.status == 'PENDING'

@pytest.mark.django_db
def test_admin_approve_extension(api_client, admin_user, vendor_profile):
    extension = StoreExtensionRequest.objects.create(vendor=vendor_profile, reason="Test Reason")
    
    api_client.force_authenticate(user=admin_user)
    url = reverse('admin-extension-approve', args=[extension.id])
    
    response = api_client.post(url)
    assert response.status_code == 200
    
    extension.refresh_from_db()
    assert extension.status == 'APPROVED'

@pytest.mark.django_db
def test_admin_reject_extension(api_client, admin_user, vendor_profile):
    extension = StoreExtensionRequest.objects.create(vendor=vendor_profile, reason="Test Reason")
    
    api_client.force_authenticate(user=admin_user)
    url = reverse('admin-extension-reject', args=[extension.id])
    
    response = api_client.post(url)
    assert response.status_code == 200
    
    extension.refresh_from_db()
    assert extension.status == 'REJECTED'
