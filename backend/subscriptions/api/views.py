from rest_framework import viewsets, permissions, exceptions, mixins
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import SubscriptionPlan, VendorSubscription
from .serializers import SubscriptionPlanSerializer, VendorSubscriptionSerializer

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

class VendorSubscriptionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = VendorSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not hasattr(self.request.user, 'vendor_profile'):
            return VendorSubscription.objects.none()
        return VendorSubscription.objects.filter(vendor=self.request.user.vendor_profile)

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'vendor_profile'):
            raise exceptions.PermissionDenied('You do not have a vendor profile.')
        
        vendor = self.request.user.vendor_profile
        plan = serializer.validated_data['plan']

        # Cancel existing active subscription
        VendorSubscription.objects.filter(vendor=vendor, status='ACTIVE').update(status='CANCELED')

        serializer.save(
            vendor=vendor,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            paid_price=plan.monthly_price,
            status='ACTIVE'
        )
