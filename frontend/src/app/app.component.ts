import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';
import { CartService } from './services/cart.service';

@Component({
  selector: 'app-root',
  template: `
    <div class="layout-wrapper">
      <nav class="navbar">
        <div class="container nav-container flex items-center">
          <a routerLink="/" class="brand">GALAXY STORE</a>

          <div class="search-bar">
            <input type="text" [(ngModel)]="searchQuery" (keyup.enter)="onSearch()" placeholder="Search products...">
            <button class="search-btn" (click)="onSearch()" aria-label="Search products">
              <svg viewBox="0 0 24 24" aria-hidden="true" class="search-icon">
                <path d="M10.5 4a6.5 6.5 0 1 0 4.03 11.6l4.43 4.43 1.41-1.41-4.43-4.43A6.5 6.5 0 0 0 10.5 4Zm0 2a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9Z"></path>
              </svg>
            </button>
          </div>

          <div class="nav-links">
            <a routerLink="/" class="nav-link" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Home</a>
            <a routerLink="/cart" class="nav-link" routerLinkActive="active">
              Cart
              <span class="cart-count" *ngIf="(cartService.cartCount$ | async) as cartCount">{{ cartCount }}</span>
            </a>

            <ng-container *ngIf="!(authService.currentUser$ | async)">
              <a routerLink="/login" class="nav-link" routerLinkActive="active">Login</a>
              <a routerLink="/register" class="nav-link" routerLinkActive="active">Create Account</a>
            </ng-container>

            <ng-container *ngIf="authService.currentUser$ | async as user">
              <span class="user-greeting">Hi, {{ user.email }}</span>
              <a routerLink="/orders" class="nav-link" routerLinkActive="active">My Orders</a>
              <a *ngIf="user.role === 'ADMIN'" routerLink="/admin" class="nav-link" routerLinkActive="active">Admin Dashboard</a>
              <a *ngIf="user.role === 'VENDOR'" routerLink="/seller/dashboard" class="nav-link" routerLinkActive="active">Store Dashboard</a>
              <a href="javascript:void(0)" class="nav-link" (click)="logout()">Logout</a>
            </ng-container>
          </div>
        </div>
      </nav>

      <main class="main-content-area">
        <router-outlet></router-outlet>
      </main>

      <footer class="footer">
        <div class="container footer-container">
          <div class="footer-brand">Galaxy E-Commerce</div>
          <div class="footer-links">
            <a href="#">About Us</a>
            <a href="#">Contact</a>
            <a href="#">Privacy Policy</a>
          </div>
          <p class="copyright">&copy; 2026 Galaxy Store. Built for the future.</p>
        </div>
      </footer>
    </div>
  `,
  styles: [`
    .layout-wrapper { min-height: 100vh; display: flex; flex-direction: column; }
    .navbar { background-color: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 50; padding: 1rem 0; transition: all 0.3s; }
    .nav-container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
    .brand { font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; }

    .search-bar { display: flex; flex: 1; max-width: 400px; margin: 0 2rem; position: relative; }
    .search-bar input { width: 100%; padding: 0.6rem 1rem; border: 1px solid rgba(0,0,0,0.1); border-radius: var(--radius-full); font-size: 0.9rem; font-family: var(--font-body); outline: none; transition: border 0.3s; }
    .search-bar input:focus { border-color: var(--primary); }
    .search-btn { align-items: center; background: none; border: none; color: var(--text-muted); cursor: pointer; display: inline-flex; justify-content: center; padding: 0.2rem; position: absolute; right: 0.6rem; top: 50%; transform: translateY(-50%); }
    .search-icon { fill: currentColor; height: 1.1rem; width: 1.1rem; }

    .nav-links { display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; }
    .nav-link { font-weight: 500; color: var(--text-muted); font-size: 0.95rem; position: relative; }
    .nav-link:hover, .nav-link.active { color: var(--primary); }
    .nav-link::after { content: ''; position: absolute; bottom: -4px; left: 0; width: 0%; height: 2px; background-color: var(--primary); transition: width 0.3s ease; border-radius: 2px; }
    .nav-link.active::after { width: 100%; }
    .user-greeting { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; margin-right: 0.5rem; border-right: 1px solid #ccc; padding-right: 1rem; }
    .cart-count { background: var(--primary); border-radius: 999px; color: white; display: inline-flex; font-size: 0.75rem; justify-content: center; margin-left: 0.45rem; min-width: 1.25rem; padding: 0.1rem 0.35rem; }

    .main-content-area { flex-grow: 1; }
    .footer { background-color: var(--dark-bg); color: var(--text-muted); padding: 4rem 0 2rem; margin-top: 4rem; }
    .footer-container { display: flex; flex-direction: column; gap: 2rem; align-items: center; }
    @media (min-width: 768px) { .footer-container { flex-direction: row; justify-content: space-between; } }
    .footer-brand { color: var(--dark-text); font-family: var(--font-heading); font-weight: 700; font-size: 1.25rem; }
    .footer-links { display: flex; gap: 1.5rem; font-size: 0.875rem; }
    .footer-links a:hover { color: var(--dark-text); }
    .copyright { font-size: 0.75rem; width: 100%; text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.05); }
    @media (min-width: 768px) { .copyright { text-align: right; margin-top: 0; padding-top: 0; border: none; width: auto; } }
  `]
})
export class AppComponent {
  searchQuery = '';

  constructor(
    public authService: AuthService,
    public cartService: CartService,
    private router: Router
  ) {}

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/search'], { queryParams: { q: this.searchQuery } });
      this.searchQuery = '';
    }
  }

  logout(): void {
    this.authService.logout();
    this.cartService.refreshCartCount();
    this.router.navigate(['/']);
  }
}
