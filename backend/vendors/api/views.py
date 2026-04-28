from rest_framework import viewsets, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from vendors.models import VendorProfile, StoreExtensionRequest
from products.models import Product
from .serializers import VendorProfileSerializer, VendorProductSerializer, StoreExtensionRequestSerializer

class PublicVendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VendorProfile.objects.filter(is_approved=True)
    serializer_class = VendorProfileSerializer

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
