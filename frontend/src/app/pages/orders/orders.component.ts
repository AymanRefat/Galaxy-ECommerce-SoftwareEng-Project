import { Component, OnInit } from '@angular/core';
import { Order } from '../../models/order.model';
import { CartService } from '../../services/cart.service';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: Order[] = [];
  loading = true;
  error = '';

  constructor(private cartService: CartService) {}

  ngOnInit(): void {
    this.cartService.getOrders().subscribe({
      next: (orders) => {
        this.orders = orders;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load your orders right now.';
        this.loading = false;
      }
    });
  }
}
