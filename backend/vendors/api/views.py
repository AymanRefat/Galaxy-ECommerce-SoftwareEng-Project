from rest_framework import viewsets, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from vendors.models import VendorProfile, StoreExtensionRequest
from products.models import Product
from .serializers import VendorProfileSerializer, VendorProductSerializer, StoreExtensionRequestSerializer

class IsVendorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_type == 'VENDOR'
        )

class PublicVendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VendorProfile.objects.filter(is_approved=True)
    serializer_class = VendorProfileSerializer

class VendorDashboardProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsVendorUser]

    def get_queryset(self):
        return VendorProfile.objects.filter(user=self.request.user)

class VendorDashboardProductViewSet(viewsets.ModelViewSet):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVendorUser]

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            raise exceptions.NotFound('Vendor profile not found.')

    def get_queryset(self):
        return Product.objects.filter(vendor=self.get_vendor_profile()).order_by('-id')

    def perform_create(self, serializer):
        vendor_profile = self.get_vendor_profile()
        if not vendor_profile.is_approved:
            raise exceptions.PermissionDenied('Your vendor account is pending approval.')
        serializer.save(vendor=vendor_profile)

class AdminVendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = VendorProfile.objects.all().order_by('-id')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        vendor = self.get_object()
        vendor.is_approved = True
        vendor.save()
        
        # Grant admin access so they can use the Vendor Dashboard
        vendor.user.is_staff = True
        vendor.user.save()
        
        return Response({'status': 'vendor approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        vendor = self.get_object()
        vendor.is_approved = False
        vendor.save()
        
        # Revoke admin access
        vendor.user.is_staff = False
        vendor.user.save()

        return Response({'status': 'vendor rejected'})

class AdminStoreExtensionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = StoreExtensionRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = StoreExtensionRequest.objects.all().order_by('-id')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        extension = self.get_object()
        extension.status = 'APPROVED'
        extension.save()
        return Response({'status': 'extension approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        extension = self.get_object()
        extension.status = 'REJECTED'
        extension.save()
        return Response({'status': 'extension rejected'})
