import pytest
from rest_framework.test import APIClient
from subscriptions.models import SubscriptionPlan, VendorSubscription
from vendors.models import VendorProfile
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def plan():
    return SubscriptionPlan.objects.create(name='Pro Plan', monthly_price='29.99')

@pytest.fixture
def vendor_user():
    return User.objects.create_user(username='v1', email='v1@test.com', password='password', user_type='VENDOR')

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name='Store 1')

@pytest.mark.django_db
class TestSubscriptionsAPI:
    def test_list_plans(self, api_client, plan):
        response = api_client.get('/api/subscriptions/plans/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_subscribe_plan(self, api_client, vendor_user, vendor_profile, plan):
        api_client.force_authenticate(user=vendor_user)
        response = api_client.post('/api/subscriptions/my-subscription/', {'plan': plan.id})
        assert response.status_code == 201
        assert response.data['status'] == 'ACTIVE'
        assert VendorSubscription.objects.count() == 1
