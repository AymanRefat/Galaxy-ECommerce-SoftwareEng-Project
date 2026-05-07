import { Component, Input } from '@angular/core';
import { Product } from '../../models/product.model';
import { CartService } from '../../services/cart.service';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.css']
})
export class ProductCardComponent {
  @Input() product!: Product;
  addingToCart = false;
  addMessage = '';

  constructor(private cartService: CartService) {}

  get primaryImageUrl(): string {
    const image = this.product.images.find((item) => item.is_primary) || this.product.images[0];
    if (!image) {
      return 'assets/placeholder.jpg';
    }

    try {
      const url = new URL(image.image);
      return url.pathname;
    } catch {
      return image.image;
    }
  }

  get formattedPrice(): string {
    return Number(this.product.price).toFixed(2);
  }

  get formattedRating(): string {
    return Number(this.product.average_rating).toFixed(1);
  }

  addToCart(): void {
    if (this.addingToCart) {
      return;
    }

    this.addingToCart = true;
    this.addMessage = '';
    this.cartService.addItem(this.product.id).subscribe({
      next: () => {
        this.addMessage = 'Added to cart';
        this.addingToCart = false;
      },
      error: (err: { error?: { detail?: string } }) => {
        this.addMessage = err.error?.detail || 'Unable to add right now';
        this.addingToCart = false;
      }
    });
  }
}
