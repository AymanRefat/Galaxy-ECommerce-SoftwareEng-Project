import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Cart, CheckoutPayload } from '../models/cart.model';
import { Order } from '../models/order.model';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private readonly cartUrl = '/api/cart/';
  private readonly ordersUrl = '/api/orders/';
  private readonly cartCountSubject = new BehaviorSubject<number>(0);

  cartCount$ = this.cartCountSubject.asObservable();

  constructor(private http: HttpClient) {
    this.refreshCartCount();
  }

  getCart(): Observable<Cart> {
    return this.http.get<Cart>(this.cartUrl).pipe(
      tap((cart) => this.cartCountSubject.next(this.getItemCount(cart)))
    );
  }

  addItem(productId: number, quantity: number = 1): Observable<unknown> {
    return this.http.post(`${this.cartUrl}add_item/`, {
      product: productId,
      quantity
    }).pipe(
      tap(() => this.refreshCartCount())
    );
  }

  checkout(payload: CheckoutPayload): Observable<Order> {
    return this.http.post<Order>(`${this.ordersUrl}checkout/`, payload).pipe(
      tap(() => this.cartCountSubject.next(0))
    );
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(this.ordersUrl);
  }

  refreshCartCount(): void {
    this.getCart().subscribe({
      error: () => this.cartCountSubject.next(0)
    });
  }

  private getItemCount(cart: Cart): number {
    return cart.items.reduce((count, item) => count + item.quantity, 0);
  }
}
