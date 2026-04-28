from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicVendorViewSet, AdminVendorViewSet, AdminStoreExtensionRequestViewSet
)

router = DefaultRouter()
router.register(r'admin/extensions', AdminStoreExtensionRequestViewSet, basename='admin-extension')
router.register(r'admin', AdminVendorViewSet, basename='admin-vendor')
router.register(r'', PublicVendorViewSet, basename='public-vendor')

urlpatterns = [
    path('', include(router.urls)),
]
