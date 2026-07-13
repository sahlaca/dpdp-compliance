import { useState } from "react";
import { login, register } from "./api";
import { APP_DISCLAIMER, APP_FEATURES, APP_TAGLINE, APP_BRAND_TITLE, AROHA_LOGO_URL, LOGIN_HEADLINE } from "./appContent";
import { setAuth, type AuthUser } from "./auth";

export function LoginPage({ onSuccess }: { onSuccess: (user: AuthUser) => void }) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result =
        mode === "login"
          ? await login(email, password)
          : await register({
              email,
              password,
              full_name: fullName,
              company_name: companyName || undefined,
            });
      setAuth(result.access_token, result.user);
      onSuccess(result.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-shell">
      <section className="login-hero">
        <div className="login-logo-wrap logo-badge">
          <img src={AROHA_LOGO_URL} alt="Aroha" />
        </div>
        <p className="eyebrow">{APP_BRAND_TITLE}</p>
        <h1>{LOGIN_HEADLINE}</h1>
        <p className="login-lead">{APP_TAGLINE}</p>
        <ul className="login-features">
          {APP_FEATURES.map((f) => (
            <li key={f}>{f}</li>
          ))}
        </ul>
        <p className="login-note">{APP_DISCLAIMER}</p>
      </section>

      <section className="login-panel card">
        <div className="auth-tabs">
          <button
            type="button"
            className={mode === "login" ? "active" : ""}
            onClick={() => setMode("login")}
          >
            Sign in
          </button>
          <button
            type="button"
            className={mode === "register" ? "active" : ""}
            onClick={() => setMode("register")}
          >
            Create account
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {mode === "register" && (
            <>
              <label>
                Full name
                <input
                  className="text-input"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Your name"
                />
              </label>
              <label>
                Company name <span className="optional">(optional)</span>
                <input
                  className="text-input"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="e.g. Sunrise Hotel"
                />
              </label>
            </>
          )}
          <label>
            Email
            <input
              className="text-input"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
            />
          </label>
          <label>
            Password
            <input
              className="text-input"
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={mode === "register" ? "Minimum 8 characters" : "Your password"}
            />
          </label>
          {error && <p className="error-banner">{error}</p>}
          <button className="btn submit-btn" type="submit" disabled={loading}>
            {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>
      </section>
    </div>
  );
}
