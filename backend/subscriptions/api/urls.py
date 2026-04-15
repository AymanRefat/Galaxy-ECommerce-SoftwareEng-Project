from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, VendorSubscriptionViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'my-subscription', VendorSubscriptionViewSet, basename='my-subscription')

urlpatterns = [
    path('', include(router.urls)),
]
