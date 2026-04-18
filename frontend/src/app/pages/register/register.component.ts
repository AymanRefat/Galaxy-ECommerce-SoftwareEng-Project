import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  template: `
    <div class="auth-container">
      <div class="auth-card" *ngIf="!successMsg">
        <h2 class="auth-title">Join Galaxy Store</h2>
        <p class="auth-subtitle">Create an account to unlock your digital world.</p>
        
        <div *ngIf="error" class="error-alert">{{ error }}</div>
        
        <form [formGroup]="registerForm" (ngSubmit)="onSubmit()">
          
          <div class="role-selector">
            <button type="button" [class.active]="registerForm.get('user_type')?.value === 'CONSUMER'" (click)="setRole('CONSUMER')" class="role-btn">Browser & Shopper</button>
            <button type="button" [class.active]="registerForm.get('user_type')?.value === 'VENDOR'" (click)="setRole('VENDOR')" class="role-btn">Store Owner</button>
          </div>

          <div class="form-group mt-4">
            <label>Username</label>
            <input type="text" formControlName="username" class="form-control" placeholder="Your username">
          </div>
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" formControlName="email" class="form-control" placeholder="you@example.com">
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" formControlName="password" class="form-control" placeholder="••••••••">
          </div>

          <div class="form-group" *ngIf="registerForm.get('user_type')?.value === 'VENDOR'">
            <label>Store Name</label>
            <input type="text" formControlName="store_name" class="form-control" placeholder="What is your store called?">
          </div>

          <button type="submit" class="btn btn-primary w-100 mt-4" [disabled]="registerForm.invalid || loading">
            {{ loading ? 'Registering...' : 'Create Account' }}
          </button>
        </form>
        
        <p class="auth-footer">Already have an account? <a routerLink="/login">Sign in</a></p>
      </div>

      <div class="auth-card text-center" *ngIf="successMsg">
        <div class="success-icon">✓</div>
        <h2 class="auth-title">Registration Complete!</h2>
        <p class="auth-subtitle">{{ successMsg }}</p>
        <button class="btn btn-primary mt-4" routerLink="/login">Go to Login</button>
      </div>
    </div>
  `,
  styles: [`
    .auth-container { display: flex; justify-content: center; align-items: center; min-height: 80vh; padding: 2rem; }
    .auth-card { background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: 3rem; width: 100%; max-width: 500px; animation: slideUp 0.4s ease-out; }
    .auth-title { font-size: 2rem; margin-bottom: 0.5rem; text-align: center; }
    .auth-subtitle { color: var(--text-muted); text-align: center; margin-bottom: 2rem; }
    
    .role-selector { display: flex; background: var(--bg-main); padding: 0.5rem; border-radius: var(--radius-md); gap: 0.5rem; }
    .role-btn { flex: 1; padding: 0.75rem; border: none; background: transparent; border-radius: var(--radius-md); font-weight: 600; color: var(--text-muted); cursor: pointer; transition: all var(--transition-fast); }
    .role-btn.active { background: white; color: var(--primary); box-shadow: var(--shadow-sm); }
    
    .form-group { margin-bottom: 1.5rem; }
    .form-group label { display: block; font-weight: 500; margin-bottom: 0.5rem; color: var(--text-main); }
    .form-control { width: 100%; padding: 0.75rem 1rem; border: 1px solid rgba(0,0,0,0.1); border-radius: var(--radius-md); font-family: var(--font-body); outline: none; transition: all var(--transition-fast); }
    .form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-light); }
    .w-100 { width: 100%; }
    .mt-4 { margin-top: 1rem; }
    .error-alert { background: #fee2e2; color: #b91c1c; padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; font-size: 0.875rem; text-align: center; }
    .auth-footer { text-align: center; margin-top: 2rem; font-size: 0.9rem; color: var(--text-muted); }
    .auth-footer a { color: var(--primary); font-weight: 600; }
    
    .text-center { text-align: center; }
    .success-icon { font-size: 4rem; color: #10b981; margin-bottom: 1rem; }
    
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  error = '';
  successMsg = '';

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.registerForm = this.fb.group({
      user_type: ['CONSUMER', Validators.required],
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      store_name: ['']
    });
  }

  setRole(role: string) {
    this.registerForm.get('user_type')?.setValue(role);
    if (role === 'VENDOR') {
      this.registerForm.get('store_name')?.setValidators([Validators.required]);
    } else {
      this.registerForm.get('store_name')?.clearValidators();
    }
    this.registerForm.get('store_name')?.updateValueAndValidity();
  }

  onSubmit() {
    if (this.registerForm.invalid) return;
    this.loading = true;
    this.error = '';
    
    // Clean payload
    const payload = { ...this.registerForm.value };
    if (!payload.store_name || payload.store_name.trim() === '') {
      delete payload.store_name;
    }
    
    this.authService.register(payload).subscribe({
      next: () => {
        this.loading = false;
        if (this.registerForm.value.user_type === 'VENDOR') {
          this.successMsg = "Seller account created successfully. Our team will review your application. You can login to check your status.";
        } else {
          this.successMsg = "Account created successfully! You can now login.";
        }
      },
      error: err => {
        console.error('Registration error:', err);
        let msg = '';
        if (err.error && typeof err.error === 'object') {
          msg = Object.entries(err.error)
            .map(([field, errors]) => `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`)
            .join(' | ');
        } else {
          msg = err.message || err.statusText || 'Unknown error';
        }
        this.error = 'Registration failed: ' + msg;
        this.loading = false;
      }
    });
  }
}
