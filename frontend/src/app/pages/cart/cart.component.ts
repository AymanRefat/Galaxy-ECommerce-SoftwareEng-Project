import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Cart, CheckoutPayload } from '../../models/cart.model';
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
  error = '';
  infoMessage = '';
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
        this.cart = cart;
        this.loading = false;
        this.infoMessage = cart.items.length > 0
          ? 'Cart quantity updates and removals still need backend APIs, so this page currently supports review and checkout only.'
          : '';
      },
      error: () => {
        this.error = 'Unable to load your cart right now.';
        this.loading = false;
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
      error: (err) => {
        this.checkoutLoading = false;
        this.error = err.error?.detail || 'Checkout failed. Try again with a valid payment token.';
      }
    });
  }

  get totalPrice(): string {
    return this.cart?.total_price || '0.00';
  }
}
