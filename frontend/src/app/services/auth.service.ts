import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = '/api/users/';
  private currentUserSubject = new BehaviorSubject<{ token: string; role: string; email: string } | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    this.checkToken();
  }

  private checkToken() {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role') || 'CONSUMER';
    const email = localStorage.getItem('user_email') || '';
    if (token && email) {
      this.currentUserSubject.next({ token, role: userRole, email });
    }
  }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}register/`, data);
  }

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}login/`, credentials).pipe(
      tap((res: any) => {
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);

        const role = res.user_type || this.decodeToken(res.access)?.user_type || 'CONSUMER';
        const email = res.email || this.decodeToken(res.access)?.email || credentials.email;
        localStorage.setItem('user_role', role);
        localStorage.setItem('user_email', email);
        this.currentUserSubject.next({ token: res.access, role, email });
      })
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_email');
    this.currentUserSubject.next(null);
  }

  getRole() {
    return localStorage.getItem('user_role');
  }

  isLoggedIn() {
    return !!localStorage.getItem('access_token');
  }

  private decodeToken(token: string): { user_type?: string; email?: string } | null {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch {
      return null;
    }
  }
}
