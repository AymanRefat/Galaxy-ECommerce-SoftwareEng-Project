import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface SellerProfile {
  id: number;
  store_name: string;
  description: string;
  is_approved: boolean;
  commission_rate: string;
  email: string;
}

interface SellerCategory {
  id: number;
  name: string;
  slug: string;
}

interface SellerProduct {
  id: number;
  name: string;
  description: string;
  price: string;
  stock_quantity: number;
  sku: string;
  average_rating: number;
  category: SellerCategory | null;
}

interface SellerOrderItem {
  id: number;
  tracking_number: string;
  customer_email: string;
  product_name: string;
  quantity: number;
  price_at_purchase: string;
  commission_amount: string;
  vendor_earnings: string;
  status: string;
}

@Component({
  selector: 'app-seller-dashboard',
  template: `
    <div class="container dashboard-shell">
      <section class="hero-card">
        <div>
          <h1 class="title">Seller Dashboard</h1>
          <p class="subtitle">Upload products, update stock, and keep customer orders moving.</p>
        </div>
        <div class="hero-meta" *ngIf="vendorProfile">
          <span class="badge" [class.badge-success]="vendorProfile.is_approved" [class.badge-warning]="!vendorProfile.is_approved">
            {{ vendorProfile.is_approved ? 'Approved seller' : 'Pending approval' }}
          </span>
          <span class="hero-stat">Commission {{ vendorProfile.commission_rate }}%</span>
        </div>
      </section>

      <div *ngIf="pageError" class="error-alert">{{ pageError }}</div>
      <div *ngIf="successMessage" class="success-banner">{{ successMessage }}</div>

      <section *ngIf="vendorProfile && !vendorProfile.is_approved" class="warning-banner">
        Your seller account is still under review. You can log in and monitor your status, but product and order management unlock after admin approval.
      </section>

      <div class="grid-layout">
        <section class="card form-card">
          <div class="section-head">
            <div>
              <h2 class="sub-title">Upload Product</h2>
              <p class="muted-copy">Add a new item to your storefront catalog.</p>
            </div>
          </div>

          <form [formGroup]="productForm" (ngSubmit)="submitProduct()" novalidate>
            <div class="form-grid">
              <div class="form-group">
                <label>Product Name</label>
                <input type="text" formControlName="name" class="form-control" placeholder="Galaxy Smartphone XYZ" [class.is-invalid]="isProductInvalid('name')">
                <span class="field-error" *ngIf="isProductInvalid('name')">Product name is required.</span>
              </div>
              <div class="form-group">
                <label>SKU</label>
                <input type="text" formControlName="sku" class="form-control" placeholder="GLX-PHN-01" [class.is-invalid]="isProductInvalid('sku')">
                <span class="field-error" *ngIf="isProductInvalid('sku')">SKU is required.</span>
              </div>
              <div class="form-group">
                <label>Category</label>
                <select formControlName="category_id" class="form-control" [class.is-invalid]="isProductInvalid('category_id')">
                  <option value="">Select a category</option>
                  <option *ngFor="let category of categories" [value]="category.id">{{ category.name }}</option>
                </select>
                <span class="field-error" *ngIf="isProductInvalid('category_id')">Please choose a category.</span>
              </div>
              <div class="form-group">
                <label>Price</label>
                <input type="number" formControlName="price" class="form-control" placeholder="0.00" [class.is-invalid]="isProductInvalid('price')">
                <span class="field-error" *ngIf="isProductInvalid('price')">Enter a non-negative price.</span>
              </div>
              <div class="form-group">
                <label>Stock Quantity</label>
                <input type="number" formControlName="stock_quantity" class="form-control" placeholder="10" [class.is-invalid]="isProductInvalid('stock_quantity')">
                <span class="field-error" *ngIf="isProductInvalid('stock_quantity')">Enter a non-negative stock quantity.</span>
              </div>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea formControlName="description" class="form-control" rows="4" placeholder="Describe the key product features..." [class.is-invalid]="isProductInvalid('description')"></textarea>
              <span class="field-error" *ngIf="isProductInvalid('description')">Description is required.</span>
            </div>

            <button class="btn btn-primary" type="submit" [disabled]="productLoading || !vendorProfile?.is_approved">
              {{ productLoading ? 'Publishing...' : 'Publish Product' }}
            </button>
          </form>
        </section>

        <section class="card">
          <div class="section-head">
            <div>
              <h2 class="sub-title">Store Summary</h2>
              <p class="muted-copy">Quick visibility into your current storefront.</p>
            </div>
          </div>

          <div class="summary-grid" *ngIf="vendorProfile">
            <article class="summary-item">
              <span class="summary-label">Store</span>
              <strong>{{ vendorProfile.store_name }}</strong>
            </article>
            <article class="summary-item">
              <span class="summary-label">Products</span>
              <strong>{{ products.length }}</strong>
            </article>
            <article class="summary-item">
              <span class="summary-label">Open Items</span>
              <strong>{{ activeOrdersCount }}</strong>
            </article>
          </div>
        </section>
      </div>

      <section class="card table-card">
        <div class="section-head">
          <div>
            <h2 class="sub-title">My Products</h2>
            <p class="muted-copy">Update stock levels directly from this table.</p>
          </div>
        </div>

        <div *ngIf="products.length === 0" class="empty-state">No products yet. Publish your first item above.</div>

        <div *ngIf="products.length > 0" class="table-container">
          <table class="dashboard-table">
            <thead>
              <tr>
                <th>SKU</th>
                <th>Product</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Rating</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let product of products">
                <td>{{ product.sku }}</td>
                <td>{{ product.name }}</td>
                <td>{{ product.category?.name || 'Uncategorized' }}</td>
                <td>\${{ product.price }}</td>
                <td>
                  <input
                    type="number"
                    class="table-input"
                    [value]="product.stock_quantity"
                    (input)="updateStockDraft(product, $any($event.target).value)">
                </td>
                <td>{{ product.average_rating || 0 | number:'1.1-1' }}</td>
                <td>
                  <button class="btn btn-secondary btn-sm" (click)="saveStock(product)" [disabled]="stockSavingId === product.id || !vendorProfile?.is_approved">
                    {{ stockSavingId === product.id ? 'Saving...' : 'Save Stock' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="card table-card">
        <div class="section-head">
          <div>
            <h2 class="sub-title">Order Management</h2>
            <p class="muted-copy">Update fulfillment status so customers can track progress.</p>
          </div>
        </div>

        <div *ngIf="orders.length === 0" class="empty-state">No vendor order items yet.</div>

        <div *ngIf="orders.length > 0" class="table-container">
          <table class="dashboard-table">
            <thead>
              <tr>
                <th>Tracking #</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Qty</th>
                <th>Status</th>
                <th>Earnings</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let order of orders">
                <td>{{ order.tracking_number }}</td>
                <td>{{ order.customer_email }}</td>
                <td>{{ order.product_name }}</td>
                <td>{{ order.quantity }}</td>
                <td>
                  <select
                    class="table-input"
                    [value]="order.status"
                    (change)="updateOrderDraft(order, $any($event.target).value)">
                    <option *ngFor="let status of orderStatuses" [value]="status">{{ status }}</option>
                  </select>
                </td>
                <td>$\{{ order.vendor_earnings }}</td>
                <td>
                  <button class="btn btn-secondary btn-sm" (click)="saveOrderStatus(order)" [disabled]="orderSavingId === order.id || !vendorProfile?.is_approved">
                    {{ orderSavingId === order.id ? 'Saving...' : 'Update' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  `,
  styles: [`
    .dashboard-shell { padding-top: 3rem; padding-bottom: 3rem; display: grid; gap: 1.5rem; }
    .hero-card, .card { background: white; border-radius: var(--radius-lg); border: 1px solid rgba(0,0,0,0.06); box-shadow: var(--shadow-sm); }
    .hero-card { align-items: start; display: flex; justify-content: space-between; gap: 1rem; padding: 2rem; }
    .hero-meta { align-items: end; display: flex; flex-direction: column; gap: 0.75rem; }
    .title { font-size: 2.5rem; letter-spacing: -0.5px; }
    .subtitle, .muted-copy { color: var(--text-muted); }
    .badge { border-radius: 999px; font-size: 0.8rem; font-weight: 700; padding: 0.35rem 0.8rem; text-transform: uppercase; }
    .badge-success { background: #dcfce7; color: #166534; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .hero-stat { color: var(--text-main); font-weight: 700; }
    .error-alert, .warning-banner, .success-banner { border-radius: var(--radius-md); padding: 1rem 1.25rem; }
    .error-alert { background: #fee2e2; color: #b91c1c; }
    .warning-banner { background: #fef3c7; color: #92400e; }
    .success-banner { background: #dcfce7; color: #166534; }
    .grid-layout { display: grid; gap: 1.5rem; }
    @media (min-width: 1024px) { .grid-layout { grid-template-columns: 1.2fr 0.8fr; } }
    .card { padding: 1.75rem; }
    .table-card { padding-bottom: 1rem; }
    .section-head { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 1.25rem; }
    .sub-title { font-size: 1.45rem; margin-bottom: 0.35rem; }
    .form-grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
    .form-group { margin-bottom: 1rem; }
    .form-group label { display: block; font-weight: 600; margin-bottom: 0.5rem; }
    .form-control, .table-input { width: 100%; border: 1px solid rgba(0,0,0,0.1); border-radius: var(--radius-md); font: inherit; padding: 0.75rem 0.9rem; }
    .summary-grid { display: grid; gap: 1rem; }
    .summary-item { background: var(--bg-main); border-radius: var(--radius-md); display: grid; gap: 0.35rem; padding: 1rem; }
    .summary-label { color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .table-container { overflow-x: auto; }
    .dashboard-table { border-collapse: collapse; width: 100%; }
    .dashboard-table th, .dashboard-table td { border-bottom: 1px solid rgba(0,0,0,0.06); padding: 0.95rem 0.75rem; text-align: left; vertical-align: middle; }
    .dashboard-table th { color: var(--text-muted); font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
    .empty-state { color: var(--text-muted); padding: 1rem 0; }
    .btn-secondary { background: var(--bg-main); color: var(--text-main); }
    .btn-sm { font-size: 0.875rem; padding: 0.6rem 1rem; }
    @media (max-width: 767px) {
      .hero-card { flex-direction: column; }
      .hero-meta { align-items: start; }
    }
  `]
})
export class SellerDashboardComponent implements OnInit {
  vendorProfile: SellerProfile | null = null;
  categories: SellerCategory[] = [];
  products: SellerProduct[] = [];
  orders: SellerOrderItem[] = [];
  productForm: FormGroup;
  productLoading = false;
  stockSavingId: number | null = null;
  orderSavingId: number | null = null;
  pageError = '';
  successMessage = '';
  orderStatuses = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'];

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.productForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      sku: ['', Validators.required],
      category_id: ['', Validators.required],
      price: ['', [Validators.required, Validators.min(0)]],
      stock_quantity: ['', [Validators.required, Validators.min(0)]],
    });
  }

  ngOnInit(): void {
    this.loadProfile();
    this.loadCategories();
    this.loadProducts();
    this.loadOrders();
  }

  loadProfile(): void {
    this.http.get<SellerProfile[]>('/api/vendors/dashboard/profile/').subscribe({
      next: (profiles) => {
        this.vendorProfile = profiles[0] || null;
      },
      error: () => {
        this.pageError = 'Unable to load seller profile.';
      }
    });
  }

  loadCategories(): void {
    this.http.get<SellerCategory[]>('/api/categories/').subscribe({
      next: (categories) => {
        this.categories = categories;
      }
    });
  }

  loadProducts(): void {
    this.http.get<SellerProduct[]>('/api/vendors/dashboard/products/').subscribe({
      next: (products) => {
        this.products = products;
      }
    });
  }

  loadOrders(): void {
    this.http.get<SellerOrderItem[]>('/api/vendors/dashboard/orders/').subscribe({
      next: (orders) => {
        this.orders = orders;
      }
    });
  }

  submitProduct(): void {
    if (this.productForm.invalid || !this.vendorProfile?.is_approved) {
      this.productForm.markAllAsTouched();
      return;
    }

    this.productLoading = true;
    this.pageError = '';
    this.successMessage = '';

    this.http.post<SellerProduct>('/api/vendors/dashboard/products/', this.productForm.value).subscribe({
      next: (product) => {
        this.products.unshift(product);
        this.productForm.reset();
        this.productLoading = false;
        this.successMessage = 'Product published successfully.';
      },
      error: (err: { error?: unknown }) => {
        this.pageError = this.formatError(err.error, 'Upload failed. Please check the form values.');
        this.productLoading = false;
      }
    });
  }

  saveStock(product: SellerProduct): void {
    if (!this.vendorProfile?.is_approved) {
      return;
    }

    this.stockSavingId = product.id;
    this.pageError = '';
    this.successMessage = '';

    this.http.patch<SellerProduct>(`/api/vendors/dashboard/products/${product.id}/`, {
      stock_quantity: Number(product.stock_quantity),
    }).subscribe({
      next: (updatedProduct) => {
        const index = this.products.findIndex((item) => item.id === updatedProduct.id);
        if (index >= 0) {
          this.products[index] = updatedProduct;
        }
        this.stockSavingId = null;
        this.successMessage = `Stock updated for ${updatedProduct.name}.`;
      },
      error: () => {
        this.pageError = 'Unable to save the stock update right now.';
        this.stockSavingId = null;
      }
    });
  }

  updateStockDraft(product: SellerProduct, rawValue: string): void {
    const parsed = Number(rawValue);
    product.stock_quantity = Number.isFinite(parsed) ? parsed : 0;
  }

  saveOrderStatus(order: SellerOrderItem): void {
    if (!this.vendorProfile?.is_approved) {
      return;
    }

    this.orderSavingId = order.id;
    this.pageError = '';
    this.successMessage = '';

    this.http.patch<SellerOrderItem>(`/api/vendors/dashboard/orders/${order.id}/`, {
      status: order.status,
    }).subscribe({
      next: (updatedOrder) => {
        const index = this.orders.findIndex((item) => item.id === updatedOrder.id);
        if (index >= 0) {
          this.orders[index] = updatedOrder;
        }
        this.orderSavingId = null;
        this.successMessage = `Order ${updatedOrder.tracking_number} updated to ${updatedOrder.status}.`;
      },
      error: () => {
        this.pageError = 'Unable to update that order status.';
        this.orderSavingId = null;
      }
    });
  }

  updateOrderDraft(order: SellerOrderItem, nextStatus: string): void {
    order.status = nextStatus;
  }

  isProductInvalid(controlName: string): boolean {
    const control = this.productForm.get(controlName);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  get activeOrdersCount(): number {
    return this.orders.filter((order) => order.status !== 'DELIVERED' && order.status !== 'CANCELLED').length;
  }

  private formatError(error: unknown, fallback: string): string {
    if (error && typeof error === 'object') {
      return Object.entries(error as Record<string, unknown>)
        .map(([field, value]) => `${field}: ${Array.isArray(value) ? value.join(', ') : value}`)
        .join(' | ');
    }
    return fallback;
  }
}
