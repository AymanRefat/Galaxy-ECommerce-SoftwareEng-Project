from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicVendorViewSet,
    AdminVendorViewSet,
    AdminStoreExtensionRequestViewSet,
    VendorDashboardProfileViewSet,
    VendorDashboardProductViewSet,
    VendorDashboardOrderViewSet,
)

router = DefaultRouter()
router.register(r'admin/extensions', AdminStoreExtensionRequestViewSet, basename='admin-extension')
router.register(r'admin', AdminVendorViewSet, basename='admin-vendor')
router.register(r'dashboard/profile', VendorDashboardProfileViewSet, basename='vendor-dashboard-profile')
router.register(r'dashboard/products', VendorDashboardProductViewSet, basename='vendor-dashboard-products')
router.register(r'dashboard/orders', VendorDashboardOrderViewSet, basename='vendor-dashboard-orders')
router.register(r'', PublicVendorViewSet, basename='public-vendor')

urlpatterns = [
    path('', include(router.urls)),
]
