import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { Category, Product } from '../../models/product.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  featuredProducts: Product[] = [];
  categories: Category[] = [];
  loading = true;
  loadError = false;

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.productService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories.slice(0, 8);
      }
    });

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
