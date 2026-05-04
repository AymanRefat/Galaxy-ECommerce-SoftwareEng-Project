import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, map, switchMap, tap } from 'rxjs';
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

  updateItemQuantity(productId: number, targetQuantity: number): Observable<Cart> {
    return this.getCart().pipe(
      switchMap((cart) => {
        const existingItem = cart.items.find((item) => item.product === productId);
        const currentQuantity = existingItem?.quantity || 0;
        const delta = targetQuantity - currentQuantity;

        if (!existingItem || delta === 0) {
          return this.getCart();
        }

        return this.addItem(productId, delta).pipe(
          switchMap(() => this.getCart())
        );
      })
    );
  }

  removeItem(productId: number): Observable<Cart> {
    return this.getCart().pipe(
      map((cart) => cart.items.find((item) => item.product === productId)?.quantity || 0),
      switchMap((quantity) => {
        if (quantity <= 0) {
          return this.getCart();
        }

        return this.addItem(productId, -quantity).pipe(
          switchMap(() => this.getCart())
        );
      })
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
