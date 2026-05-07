import uuid
from rest_framework import viewsets, permissions, status, decorators, response
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from orders.models import Cart, CartItem, Order, OrderItem, Transaction
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from products.models import Product

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return response.Response(serializer.data)

    @decorators.action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = get_or_create_cart(request)
        product_id = request.data.get('product')
        if not product_id:
             return response.Response({"detail": "product ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return response.Response({"detail": "Quantity must be a whole number."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity == 0:
            return response.Response({"detail": "Quantity change cannot be zero."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        target_quantity = quantity if created else cart_item.quantity + quantity

        if target_quantity <= 0:
            if created:
                cart_item.delete()
            else:
                cart_item.delete()
            return response.Response({"detail": "Item removed from cart."}, status=status.HTTP_200_OK)

        if target_quantity > product.stock_quantity:
            return response.Response(
                {"detail": f"Only {product.stock_quantity} item(s) of {product.name} are available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = target_quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @decorators.action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = get_or_create_cart(request)
        cart.items.filter(quantity__lte=0).delete()
        active_items = cart.items.select_related('product__vendor').filter(quantity__gt=0)

        if not active_items.exists():
            return response.Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        payment_token = request.data.get('payment_token')
        shipping_address = request.data.get('shipping_address')
        if not payment_token:
            return response.Response({"detail": "Payment token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Mock payment gateway verification
        payment_status = 'SUCCESS' if payment_token != 'FAIL_TOKEN' else 'FAILED'

        for item in active_items:
            if item.product.stock_quantity < item.quantity:
                return response.Response(
                    {"detail": f"Only {item.product.stock_quantity} item(s) of {item.product.name} are still available."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        total_amount = sum(item.product.price * item.quantity for item in active_items)
        
        with db_transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                tracking_number=str(uuid.uuid4()).split('-')[0].upper(),
                shipping_address=shipping_address or None,
            )

            # Create Transaction Record
            Transaction.objects.create(
                order=order,
                transaction_id=f"txn_{uuid.uuid4().hex[:16]}",
                amount=total_amount,
                status=payment_status
            )

            if payment_status == 'FAILED':
                order.status = 'CANCELLED'
                order.save()
                return response.Response({"detail": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

            for item in active_items:
                product = item.product
                product.stock_quantity -= item.quantity
                product.save()

                # Calculate Commission
                vendor = product.vendor
                commission_rate = vendor.commission_rate if vendor else 10.00
                price_at_purchase = product.price
                total_item_price = price_at_purchase * item.quantity
                commission_amount = (total_item_price * commission_rate) / 100
                vendor_earnings = total_item_price - commission_amount

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    vendor=vendor,
                    quantity=item.quantity,
                    price_at_purchase=price_at_purchase,
                    commission_amount=commission_amount,
                    vendor_earnings=vendor_earnings
                )

            cart.items.all().delete()

        serializer = OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
