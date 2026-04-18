import { Component, Input } from '@angular/core';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.css']
})
export class ProductCardComponent {
  @Input() product!: Product;

  get primaryImageUrl(): string {
    const img = this.product.images.find(i => i.is_primary) || this.product.images[0];
    if (!img) return 'assets/placeholder.jpg';
    // Backend returns absolute URLs like http://localhost:8000/media/...
    // Strip the origin so the path is relative (works via Nginx proxy on port 80)
    try {
      const url = new URL(img.image);
      return url.pathname;
    } catch {
      return img.image;
    }
  }

  get formattedPrice(): string {
    return Number(this.product.price).toFixed(2);
  }

  get formattedRating(): string {
    return Number(this.product.average_rating).toFixed(1);
  }
}
