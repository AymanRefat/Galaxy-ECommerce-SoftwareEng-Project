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
        
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
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
        if not cart.items.exists():
            return response.Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        payment_token = request.data.get('payment_token')
        if not payment_token:
            return response.Response({"detail": "Payment token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Mock payment gateway verification
        payment_status = 'SUCCESS' if payment_token != 'FAIL_TOKEN' else 'FAILED'

        total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
        
        with db_transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                tracking_number=str(uuid.uuid4()).split('-')[0].upper()
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

            for item in cart.items.all():
                product = item.product
                # Deduct stock
                if product.stock_quantity < item.quantity:
                    raise Exception(f"Not enough stock for {product.name}")
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
