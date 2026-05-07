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
def category():
    return Category.objects.create(name='Electronics', slug='electronics')


@pytest.fixture
def vendor_user():
    return User.objects.create_user(
        username='vendor1',
        email='vendor1@example.com',
        password='password',
        user_type='VENDOR',
    )


@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name='Store 1', is_approved=True, commission_rate=12.50)


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123',
    )


@pytest.mark.django_db
class TestVendorAPI:
    def test_list_public_vendors(self, api_client, vendor_profile):
        response = api_client.get('/api/vendors/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['store_name'] == 'Store 1'

    def test_vendor_can_create_product_from_dashboard(self, api_client, vendor_user, vendor_profile, category):
        api_client.force_authenticate(user=vendor_user)
        response = api_client.post('/api/vendors/dashboard/products/', {
            'name': 'Galaxy Keyboard',
            'description': 'Mechanical keyboard',
            'price': '250.00',
            'stock_quantity': 9,
            'sku': 'KEY-001',
            'category_id': category.id,
        }, format='json')

        assert response.status_code == 201
        product = Product.objects.get(sku='KEY-001')
        assert product.vendor == vendor_profile
        assert product.category == category

    def test_vendor_can_update_stock_from_dashboard(self, api_client, vendor_user, vendor_profile, category):
        product = Product.objects.create(
            vendor=vendor_profile,
            category=category,
            name='Mouse',
            description='Wireless mouse',
            price='99.99',
            stock_quantity=4,
            sku='MOUSE-001',
        )

        api_client.force_authenticate(user=vendor_user)
        response = api_client.patch(f'/api/vendors/dashboard/products/{product.id}/', {
            'stock_quantity': 12,
        }, format='json')

        assert response.status_code == 200
        product.refresh_from_db()
        assert product.stock_quantity == 12

    def test_vendor_can_manage_order_status(self, api_client, vendor_user, vendor_profile, category):
        consumer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='password',
            user_type='CONSUMER',
        )
        product = Product.objects.create(
            vendor=vendor_profile,
            category=category,
            name='Monitor',
            description='4K display',
            price='500.00',
            stock_quantity=7,
            sku='MON-001',
        )
        order = Order.objects.create(user=consumer, tracking_number='TRACK123', total_amount='500.00')
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            vendor=vendor_profile,
            quantity=1,
            price_at_purchase='500.00',
            commission_amount='62.50',
            vendor_earnings='437.50',
        )

        api_client.force_authenticate(user=vendor_user)
        response = api_client.patch(f'/api/vendors/dashboard/orders/{order_item.id}/', {
            'status': 'SHIPPED',
        }, format='json')

        assert response.status_code == 200
        order_item.refresh_from_db()
        order.refresh_from_db()
        assert order_item.status == 'SHIPPED'
        assert order.status == 'SHIPPED'

    def test_admin_can_update_vendor_commission_rate(self, api_client, admin_user, vendor_profile):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(f'/api/vendors/admin/{vendor_profile.id}/', {
            'commission_rate': '7.50',
        }, format='json')

        assert response.status_code == 200
        vendor_profile.refresh_from_db()
        assert str(vendor_profile.commission_rate) == '7.50'
