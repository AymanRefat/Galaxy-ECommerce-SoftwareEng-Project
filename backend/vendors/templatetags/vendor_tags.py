from django import template
from django.db.models import Sum
from orders.models import OrderItem
from subscriptions.models import VendorSubscription

register = template.Library()

@register.simple_tag(takes_context=True)
def get_vendor_stats(context):
    request = context.get('request')
    if not request or not hasattr(request.user, 'vendor_profile'):
        return None
    
    vendor = request.user.vendor_profile
    
    items = OrderItem.objects.filter(vendor=vendor)
    # Revenue after commission
    total_earnings = items.aggregate(total=Sum('vendor_earnings'))['total'] or 0.00
    items_sold = items.aggregate(total=Sum('quantity'))['total'] or 0
    
    active_subscriptions = VendorSubscription.objects.filter(vendor=vendor, status='ACTIVE').count()
    
    return {
        'total_earnings': total_earnings,
        'items_sold': items_sold,
        'active_subscriptions': active_subscriptions,
        'store_name': vendor.store_name,
    }
