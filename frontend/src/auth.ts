const TOKEN_KEY = "dpdp_access_token";
const USER_KEY = "dpdp_user";

export interface AuthUser {
  id: number;
  email: string;
  full_name: string;
  company_name: string | null;
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function getUser(): AuthUser | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

export function setAuth(token: string, user: AuthUser): void {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

/** First name, or company name if no personal name is stored. */
export function welcomeDisplayName(user: AuthUser): string | null {
  const fullName = user.full_name?.trim();
  if (fullName) return fullName.split(/\s+/)[0];
  const company = user.company_name?.trim();
  if (company) return company;
  return null;
}

export function authHeaders(): HeadersInit {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
