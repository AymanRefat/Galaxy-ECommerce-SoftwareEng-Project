import pytest
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import VendorSubscription, SubscriptionPlan
from vendors.models import VendorProfile
from users.models import User
from io import StringIO

@pytest.fixture
def plan():
    return SubscriptionPlan.objects.create(name="Premium", monthly_price=50.00)

@pytest.fixture
def vendor_user():
    return User.objects.create_user(email="vendor@example.com", username="vendoruser", password="password123")

@pytest.fixture
def vendor_profile(vendor_user):
    return VendorProfile.objects.create(user=vendor_user, store_name="Test Store", is_approved=True)

@pytest.mark.django_db
def test_check_expired_subscriptions(vendor_profile, plan):
    # Create an active subscription that is already past due
    past_due_date = timezone.now() - timedelta(days=1)
    
    subscription = VendorSubscription.objects.create(
        vendor=vendor_profile,
        plan=plan,
        start_date=timezone.now() - timedelta(days=31),
        end_date=past_due_date,
        paid_price=50.00,
        status='ACTIVE'
    )
    
    out = StringIO()
    call_command('check_expired_subscriptions', stdout=out)
    
    subscription.refresh_from_db()
    
    assert subscription.status == 'PAST_DUE'
    assert 'Successfully processed 1 expired subscriptions' in out.getvalue()

@pytest.mark.django_db
def test_check_expired_subscriptions_ignores_valid(vendor_profile, plan):
    # Create an active subscription that is still valid
    future_date = timezone.now() + timedelta(days=10)
    
    subscription = VendorSubscription.objects.create(
        vendor=vendor_profile,
        plan=plan,
        start_date=timezone.now() - timedelta(days=10),
        end_date=future_date,
        paid_price=50.00,
        status='ACTIVE'
    )
    
    out = StringIO()
    call_command('check_expired_subscriptions', stdout=out)
    
    subscription.refresh_from_db()
    
    assert subscription.status == 'ACTIVE'
    assert 'Successfully processed 0 expired subscriptions' in out.getvalue()
