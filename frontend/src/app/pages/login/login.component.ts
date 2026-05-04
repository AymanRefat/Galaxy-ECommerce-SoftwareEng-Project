import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  template: `
    <div class="auth-container">
      <div class="auth-card">
        <h2 class="auth-title">Welcome Back</h2>
        <p class="auth-subtitle">Login to your Galaxy Store account.</p>

        <div *ngIf="error" class="error-alert">{{ error }}</div>

        <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" formControlName="email" class="form-control" placeholder="you@example.com">
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" formControlName="password" class="form-control" placeholder="Enter your password">
          </div>
          <button type="submit" class="btn btn-primary w-100 mt-4" [disabled]="loginForm.invalid || loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <p class="auth-footer">Don't have an account? <a routerLink="/register">Register here</a></p>
      </div>
    </div>
  `,
  styles: [`
    .auth-container { display: flex; justify-content: center; align-items: center; min-height: 80vh; padding: 2rem; }
    .auth-card { background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: 3rem; width: 100%; max-width: 450px; animation: slideUp 0.4s ease-out; }
    .auth-title { font-size: 2rem; margin-bottom: 0.5rem; text-align: center; }
    .auth-subtitle { color: var(--text-muted); text-align: center; margin-bottom: 2rem; }
    .form-group { margin-bottom: 1.5rem; }
    .form-group label { display: block; font-weight: 500; margin-bottom: 0.5rem; color: var(--text-main); }
    .form-control { width: 100%; padding: 0.75rem 1rem; border: 1px solid rgba(0,0,0,0.1); border-radius: var(--radius-md); font-family: var(--font-body); outline: none; transition: all var(--transition-fast); }
    .form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-light); }
    .w-100 { width: 100%; }
    .mt-4 { margin-top: 1rem; }
    .error-alert { background: #fee2e2; color: #b91c1c; padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; font-size: 0.875rem; text-align: center; }
    .auth-footer { text-align: center; margin-top: 2rem; font-size: 0.9rem; color: var(--text-muted); }
    .auth-footer a { color: var(--primary); font-weight: 600; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class LoginComponent {
  loginForm: FormGroup;
  loading = false;
  error = '';
  private returnUrl = '/';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    this.returnUrl = this.route.snapshot.queryParamMap.get('returnUrl') || '/';
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';

    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        const role = this.authService.getRole();
        if (this.returnUrl !== '/') {
          this.router.navigateByUrl(this.returnUrl);
          return;
        }

        if (role === 'ADMIN') {
          this.router.navigate(['/admin']);
        } else if (role === 'VENDOR') {
          this.router.navigate(['/seller/dashboard']);
        } else {
          this.router.navigate(['/']);
        }
      },
      error: (err) => {
        this.error = err.error?.detail || 'Invalid login credentials.';
        this.loading = false;
      }
    });
  }
}
