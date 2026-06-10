import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("demo@podlens.app");
  const [password, setPassword] = useState("podlens-demo");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Login failed. Check your credentials."
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <div className="brand" style={{ fontSize: 28, marginBottom: 8 }}>
        🎙️ PodLens
      </div>
      <p className="muted" style={{ marginTop: 0 }}>
        Podcast analytics across Spotify, YouTube &amp; Apple.
      </p>
      <form onSubmit={onSubmit} className="panel">
        <h2>Sign in</h2>
        {error && <div className="error">{error}</div>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
        <p className="muted" style={{ fontSize: 12, marginBottom: 0 }}>
          Demo seeded account is prefilled.
        </p>
      </form>
    </div>
  );
}
