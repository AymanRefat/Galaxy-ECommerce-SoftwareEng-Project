import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface AdminVendor {
  id: number;
  store_name: string;
  is_approved: boolean;
  commission_rate: string;
  email: string;
}

@Component({
  selector: 'app-admin-dashboard',
  template: `
    <div class="container dashboard-shell">
      <section class="hero-card">
        <div>
          <h1 class="title">Admin Dashboard</h1>
          <p class="subtitle">Approve sellers and manage the commission model for each storefront.</p>
        </div>
      </section>

      <div *ngIf="pageError" class="error-alert">{{ pageError }}</div>
      <div *ngIf="successMessage" class="success-banner">{{ successMessage }}</div>

      <section class="card">
        <div class="section-head">
          <div>
            <h2 class="sub-title">Vendor Applications and Commission Rates</h2>
            <p class="muted-copy">Moderate new sellers and adjust revenue percentages for future transactions.</p>
          </div>
        </div>

        <div *ngIf="loading" class="empty-state">Loading vendors...</div>
        <div *ngIf="!loading && vendors.length === 0" class="empty-state">No vendors found.</div>

        <div *ngIf="!loading && vendors.length > 0" class="table-container">
          <table class="dashboard-table">
            <thead>
              <tr>
                <th>Store</th>
                <th>Email</th>
                <th>Status</th>
                <th>Commission %</th>
                <th>Moderation</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let vendor of vendors">
                <td>{{ vendor.store_name }}</td>
                <td>{{ vendor.email }}</td>
                <td>
                  <span class="badge" [class.badge-success]="vendor.is_approved" [class.badge-warning]="!vendor.is_approved">
                    {{ vendor.is_approved ? 'Approved' : 'Pending' }}
                  </span>
                </td>
                <td>
                  <input
                    type="number"
                    class="table-input"
                    [value]="vendor.commission_rate"
                    (input)="updateCommissionDraft(vendor, $any($event.target).value)">
                </td>
                <td class="actions-cell">
                  <button *ngIf="!vendor.is_approved" class="btn btn-success btn-sm" (click)="approve(vendor)" [disabled]="actionVendorId === vendor.id">
                    Approve
                  </button>
                  <button *ngIf="vendor.is_approved" class="btn btn-alert btn-sm" (click)="reject(vendor)" [disabled]="actionVendorId === vendor.id">
                    Revoke
                  </button>
                </td>
                <td>
                  <button class="btn btn-secondary btn-sm" (click)="saveCommission(vendor)" [disabled]="actionVendorId === vendor.id">
                    {{ actionVendorId === vendor.id ? 'Saving...' : 'Save Rate' }}
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
    .hero-card, .card { padding: 2rem; }
    .title { font-size: 2.5rem; letter-spacing: -0.5px; }
    .subtitle, .muted-copy, .empty-state { color: var(--text-muted); }
    .section-head { margin-bottom: 1.25rem; }
    .sub-title { font-size: 1.45rem; margin-bottom: 0.35rem; }
    .error-alert, .success-banner { border-radius: var(--radius-md); padding: 1rem 1.25rem; }
    .error-alert { background: #fee2e2; color: #b91c1c; }
    .success-banner { background: #dcfce7; color: #166534; }
    .table-container { overflow-x: auto; }
    .dashboard-table { border-collapse: collapse; width: 100%; }
    .dashboard-table th, .dashboard-table td { border-bottom: 1px solid rgba(0,0,0,0.06); padding: 0.95rem 0.75rem; text-align: left; vertical-align: middle; }
    .dashboard-table th { color: var(--text-muted); font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
    .table-input { width: 120px; border: 1px solid rgba(0,0,0,0.1); border-radius: var(--radius-md); font: inherit; padding: 0.7rem 0.8rem; }
    .badge { border-radius: 999px; font-size: 0.8rem; font-weight: 700; padding: 0.35rem 0.8rem; text-transform: uppercase; }
    .badge-success { background: #dcfce7; color: #166534; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .actions-cell { display: flex; gap: 0.75rem; }
    .btn-sm { font-size: 0.875rem; padding: 0.6rem 1rem; }
    .btn-success { background: #10b981; color: white; }
    .btn-alert { background: #ef4444; color: white; }
    .btn-secondary { background: var(--bg-main); color: var(--text-main); }
  `]
})
export class AdminDashboardComponent implements OnInit {
  vendors: AdminVendor[] = [];
  loading = true;
  actionVendorId: number | null = null;
  pageError = '';
  successMessage = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadVendors();
  }

  loadVendors(): void {
    this.loading = true;
    this.http.get<AdminVendor[]>('/api/vendors/admin/').subscribe({
      next: (vendors) => {
        this.vendors = vendors;
        this.loading = false;
      },
      error: () => {
        this.pageError = 'Unable to load vendors right now.';
        this.loading = false;
      }
    });
  }

  approve(vendor: AdminVendor): void {
    this.actionVendorId = vendor.id;
    this.pageError = '';
    this.successMessage = '';

    this.http.post(`/api/vendors/admin/${vendor.id}/approve/`, {}).subscribe({
      next: () => {
        this.actionVendorId = null;
        this.successMessage = `${vendor.store_name} approved successfully.`;
        this.loadVendors();
      },
      error: () => {
        this.pageError = 'Unable to approve that seller.';
        this.actionVendorId = null;
      }
    });
  }

  reject(vendor: AdminVendor): void {
    this.actionVendorId = vendor.id;
    this.pageError = '';
    this.successMessage = '';

    this.http.post(`/api/vendors/admin/${vendor.id}/reject/`, {}).subscribe({
      next: () => {
        this.actionVendorId = null;
        this.successMessage = `${vendor.store_name} approval was revoked.`;
        this.loadVendors();
      },
      error: () => {
        this.pageError = 'Unable to revoke that seller approval.';
        this.actionVendorId = null;
      }
    });
  }

  saveCommission(vendor: AdminVendor): void {
    this.actionVendorId = vendor.id;
    this.pageError = '';
    this.successMessage = '';

    this.http.patch<AdminVendor>(`/api/vendors/admin/${vendor.id}/`, {
      commission_rate: vendor.commission_rate,
    }).subscribe({
      next: () => {
        this.actionVendorId = null;
        this.successMessage = `Commission rate saved for ${vendor.store_name}.`;
        this.loadVendors();
      },
      error: () => {
        this.pageError = 'Unable to save that commission rate.';
        this.actionVendorId = null;
      }
    });
  }

  updateCommissionDraft(vendor: AdminVendor, rawValue: string): void {
    vendor.commission_rate = rawValue;
  }
}
