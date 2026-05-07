from rest_framework import viewsets, permissions, exceptions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from vendors.models import VendorProfile, StoreExtensionRequest
from products.models import Product
from orders.models import OrderItem
from .serializers import (
    VendorProfileSerializer,
    VendorProductSerializer,
    StoreExtensionRequestSerializer,
    VendorOrderItemSerializer,
)


class IsVendorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'user_type', None) == 'VENDOR'
            and hasattr(request.user, 'vendor_profile')
        )


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

        vendor.user.is_staff = True
        vendor.user.save()
        return Response({'status': 'vendor approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        vendor = self.get_object()
        vendor.is_approved = False
        vendor.save()

        vendor.user.is_staff = False
        vendor.user.save()
        return Response({'status': 'vendor rejected'})


class VendorDashboardProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsVendorUser]

    def list(self, request):
        serializer = VendorProfileSerializer(request.user.vendor_profile)
        return Response([serializer.data])


class VendorDashboardProductViewSet(viewsets.ModelViewSet):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVendorUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor_profile).order_by('-created_at')

    def perform_create(self, serializer):
        vendor = self.request.user.vendor_profile
        if not vendor.is_approved:
            raise exceptions.PermissionDenied('Your vendor account is still pending approval.')
        serializer.save(vendor=vendor)

    def perform_update(self, serializer):
        vendor = self.request.user.vendor_profile
        if not vendor.is_approved:
            raise exceptions.PermissionDenied('Your vendor account is still pending approval.')
        serializer.save()


class VendorDashboardOrderViewSet(viewsets.ModelViewSet):
    serializer_class = VendorOrderItemSerializer
    permission_classes = [IsVendorUser]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return OrderItem.objects.filter(vendor=self.request.user.vendor_profile).select_related(
            'order', 'product', 'order__user'
        ).order_by('-order__created_at', '-id')

    def perform_update(self, serializer):
        if not self.request.user.vendor_profile.is_approved:
            raise exceptions.PermissionDenied('Your vendor account is still pending approval.')
        order_item = serializer.save()
        self._sync_parent_order_status(order_item)

    def _sync_parent_order_status(self, order_item):
        order = order_item.order
        statuses = list(order.items.values_list('status', flat=True))
        if not statuses:
            order.status = 'PENDING'
        elif all(status == 'CANCELLED' for status in statuses):
            order.status = 'CANCELLED'
        elif all(status == 'DELIVERED' for status in statuses):
            order.status = 'DELIVERED'
        elif any(status == 'SHIPPED' for status in statuses):
            order.status = 'SHIPPED'
        elif any(status == 'PROCESSING' for status in statuses):
            order.status = 'PROCESSING'
        else:
            order.status = 'PENDING'
        order.save(update_fields=['status'])


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
