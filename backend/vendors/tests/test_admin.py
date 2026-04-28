import pytest
from django.urls import reverse
from django.contrib.admin.sites import site
from rest_framework.test import APIClient
from users.models import User
from vendors.models import VendorProfile
from products.models import Product, Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(email="admin@example.com", username="admin", password="password123")

@pytest.fixture
def vendor_user():
    return User.objects.create_user(email="vendor@example.com", username="vendoruser", password="password123", is_staff=True)

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name="Test Store", is_approved=True)

@pytest.fixture
def other_vendor_user():
    return User.objects.create_user(email="other@example.com", username="othervendor", password="password123", is_staff=True)

@pytest.fixture
def other_vendor_profile(other_vendor_user):
    return VendorProfile.objects.create(user=other_vendor_user, store_name="Other Store", is_approved=True)

@pytest.mark.django_db
def test_vendor_admin_sees_only_own_products(api_client, vendor_user, vendor_profile, other_vendor_profile):
    api_client.force_login(vendor_user)
    
    category = Category.objects.create(name="Electronics", slug="electronics")
    p1 = Product.objects.create(vendor=vendor_profile, category=category, name="My Product", price=10.0, stock_quantity=5, sku="1")
    p2 = Product.objects.create(vendor=other_vendor_profile, category=category, name="Other Product", price=10.0, stock_quantity=5, sku="2")
    
    url = reverse('admin:products_product_changelist')
    response = api_client.get(url)
    
    assert response.status_code == 200
    # Vendor should see their product
    assert "My Product" in response.content.decode()
    # Vendor should NOT see the other vendor's product
    assert "Other Product" not in response.content.decode()

@pytest.mark.django_db
def test_admin_sees_all_products(api_client, admin_user, vendor_profile, other_vendor_profile):
    api_client.force_login(admin_user)
    
    category = Category.objects.create(name="Electronics", slug="electronics")
    p1 = Product.objects.create(vendor=vendor_profile, category=category, name="My Product", price=10.0, stock_quantity=5, sku="1")
    p2 = Product.objects.create(vendor=other_vendor_profile, category=category, name="Other Product", price=10.0, stock_quantity=5, sku="2")
    
    url = reverse('admin:products_product_changelist')
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert "My Product" in response.content.decode()
    assert "Other Product" in response.content.decode()

@pytest.mark.django_db
def test_vendor_auto_assign_product(api_client, vendor_user, vendor_profile):
    api_client.force_login(vendor_user)
    
    category = Category.objects.create(name="Electronics", slug="electronics")
    url = reverse('admin:products_product_add')
    
    data = {
        'category': category.id,
        'name': 'New Auto Product',
        'description': 'Test',
        'price': '50.00',
        'stock_quantity': '10',
        'sku': 'AUTO-01',
    }
    
    response = api_client.post(url, data, follow=True)
    assert response.status_code == 200
    
    product = Product.objects.get(name='New Auto Product')
    assert product.vendor == vendor_profile

@pytest.mark.django_db
def test_vendor_admin_index_stats(api_client, vendor_user, vendor_profile):
    api_client.force_login(vendor_user)
    url = reverse('admin:index')
    response = api_client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert vendor_profile.store_name in content
    assert 'Total Earnings' in content
    assert 'Items Sold' in content
    assert 'Active Subscriptions' in content
