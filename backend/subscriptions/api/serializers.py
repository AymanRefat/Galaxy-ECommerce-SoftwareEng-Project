from rest_framework import serializers
from subscriptions.models import SubscriptionPlan, VendorSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'monthly_price', 'features']

class VendorSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    
    class Meta:
        model = VendorSubscription
        fields = ['id', 'plan', 'plan_name', 'status', 'start_date', 'end_date', 'paid_price']
        read_only_fields = ['status', 'start_date', 'end_date', 'paid_price']
