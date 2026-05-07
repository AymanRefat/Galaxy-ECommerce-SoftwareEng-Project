import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Cart, CartItem, CheckoutPayload } from '../../models/cart.model';
import { CartService } from '../../services/cart.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
  cart: Cart | null = null;
  checkoutForm: FormGroup;
  loading = true;
  checkoutLoading = false;
  updatingProductId: number | null = null;
  error = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private cartService: CartService,
    private authService: AuthService,
    private router: Router
  ) {
    this.checkoutForm = this.fb.group({
      full_name: ['', Validators.required],
      phone: ['', Validators.required],
      city: ['', Validators.required],
      address_line: ['', Validators.required],
      payment_token: ['VALID_TOKEN', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.loading = true;
    this.cartService.getCart().subscribe({
      next: (cart) => {
        this.cart = this.normalizeCart(cart);
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load your cart right now.';
        this.loading = false;
      }
    });
  }

  changeQuantity(item: CartItem, nextQuantity: number): void {
    if (nextQuantity < 1 || this.updatingProductId !== null) {
      return;
    }

    this.updatingProductId = item.product;
    this.error = '';
    this.cartService.updateItemQuantity(item.product, nextQuantity).subscribe({
      next: (cart) => {
        this.cart = this.normalizeCart(cart);
        this.updatingProductId = null;
      },
      error: (err: { error?: { detail?: string } }) => {
        this.error = err.error?.detail || 'Unable to update that cart item right now.';
        this.updatingProductId = null;
      }
    });
  }

  removeItem(item: CartItem): void {
    if (this.updatingProductId !== null) {
      return;
    }

    this.updatingProductId = item.product;
    this.error = '';
    this.cartService.removeItem(item.product).subscribe({
      next: (cart) => {
        this.cart = this.normalizeCart(cart);
        this.updatingProductId = null;
      },
      error: (err: { error?: { detail?: string } }) => {
        this.error = err.error?.detail || 'Unable to remove that cart item right now.';
        this.updatingProductId = null;
      }
    });
  }

  checkout(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login'], { queryParams: { returnUrl: '/cart' } });
      return;
    }

    if (this.checkoutForm.invalid || !this.cart || this.cart.items.length === 0) {
      this.checkoutForm.markAllAsTouched();
      return;
    }

    this.checkoutLoading = true;
    this.error = '';

    const payload: CheckoutPayload = {
      payment_token: this.checkoutForm.value.payment_token,
      shipping_address: {
        full_name: this.checkoutForm.value.full_name,
        phone: this.checkoutForm.value.phone,
        city: this.checkoutForm.value.city,
        address_line: this.checkoutForm.value.address_line
      }
    };

    this.cartService.checkout(payload).subscribe({
      next: (order) => {
        this.checkoutLoading = false;
        this.successMessage = `Order ${order.tracking_number} placed successfully.`;
        this.checkoutForm.reset({ payment_token: 'VALID_TOKEN' });
        this.loadCart();
      },
      error: (err: { error?: { detail?: string } }) => {
        this.checkoutLoading = false;
        this.error = err.error?.detail || 'Checkout failed. Try again with a valid payment token.';
      }
    });
  }

  isInvalid(controlName: string): boolean {
    const control = this.checkoutForm.get(controlName);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  get totalPrice(): string {
    return this.cart?.total_price || '0.00';
  }

  getLineTotal(item: CartItem): string {
    return (Number(item.price) * item.quantity).toFixed(2);
  }

  private normalizeCart(cart: Cart): Cart {
    const items = cart.items.filter((item) => item.quantity > 0);
    const total = items.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0);

    return {
      ...cart,
      items,
      total_price: total.toFixed(2)
    };
  }
}
