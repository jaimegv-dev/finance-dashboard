import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

interface LoginResponse {
  access: string;
  refresh: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root'
})
export class Auth {
  private http = inject(HttpClient);

  private apiUrl = 'http://127.0.0.1:8000/api';

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(
      `${this.apiUrl}/token/`,
      { username, password }
    ).pipe(
      tap(response => {
        localStorage.setItem('access', response.access);
        localStorage.setItem('refresh', response.refresh);
      })
    );
  }

  register(data: RegisterData): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, data);
  }

  logout(): void {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access');
  }

  isLoggedIn(): boolean {
    return this.getAccessToken() !== null;
  }
}
