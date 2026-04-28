import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Cart, CartItem, Order, OrderItem, Transaction
from products.models import Product, Category
from vendors.models import VendorProfile
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(email="test@example.com", username="testuser", password="password123")

@pytest.fixture
def vendor_user():
    user = User.objects.create_user(email="vendor@example.com", username="vendoruser", password="password123")
    return user

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name="Test Store", is_approved=True, commission_rate=15.00)

@pytest.fixture
def product(vendor_profile):
    category = Category.objects.create(name="Test Category", slug="test-category")
    return Product.objects.create(
        vendor=vendor_profile,
        category=category,
        name="Test Product",
        description="A great product",
        price=100.00,
        stock_quantity=10,
        sku="TEST-SKU-001"
    )

@pytest.mark.django_db
def test_successful_checkout(api_client, user, product):
    api_client.force_authenticate(user=user)
    
    # 1. Add item to cart
    add_cart_url = reverse('cart-add-item')
    api_client.post(add_cart_url, {'product': product.id, 'quantity': 2})
    
    cart = Cart.objects.get(user=user)
    assert cart.items.count() == 1

    # 2. Checkout
    checkout_url = reverse('order-checkout')
    response = api_client.post(checkout_url, {'payment_token': 'VALID_TOKEN'})
    
    assert response.status_code == 201
    
    # Verify Order
    order = Order.objects.get(user=user)
    assert order.total_amount == 200.00
    
    # Verify Transaction
    transaction = Transaction.objects.get(order=order)
    assert transaction.status == 'SUCCESS'
    assert transaction.amount == 200.00
    
    # Verify Stock Deduction
    product.refresh_from_db()
    assert product.stock_quantity == 8

    # Verify Commission
    order_item = OrderItem.objects.get(order=order)
    assert order_item.commission_amount == 30.00  # 15% of 200
    assert order_item.vendor_earnings == 170.00
    
    # Cart should be empty
    assert cart.items.count() == 0

@pytest.mark.django_db
def test_failed_checkout(api_client, user, product):
    api_client.force_authenticate(user=user)
    add_cart_url = reverse('cart-add-item')
    api_client.post(add_cart_url, {'product': product.id, 'quantity': 1})
    
    checkout_url = reverse('order-checkout')
    response = api_client.post(checkout_url, {'payment_token': 'FAIL_TOKEN'})
    
    assert response.status_code == 400
    
    order = Order.objects.get(user=user)
    assert order.status == 'CANCELLED'
    
    transaction = Transaction.objects.get(order=order)
    assert transaction.status == 'FAILED'
    
    # Stock should not be deducted
    product.refresh_from_db()
    assert product.stock_quantity == 10
