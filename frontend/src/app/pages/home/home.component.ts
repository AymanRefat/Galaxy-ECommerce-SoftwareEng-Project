import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  featuredProducts: Product[] = [];
  loading = true;
  loadError = false;
  categories = [
    { name: 'Electronics', slug: 'electronics' },
    { name: 'Accessories', slug: 'accessories' },
    { name: 'Furniture', slug: 'furniture' },
    { name: 'Home Goods', slug: 'home-goods' }
  ];

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.featuredProducts = products.slice(0, 4);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error fetching featured products:', err);
        this.loading = false;
        this.loadError = true;
      }
    });
  }
}
