import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext.jsx";

export default function AppLayout() {
  const { user, logout } = useAuth();
  return (
    <div className="app-shell">
      <nav className="nav">
        <div className="brand">🎙️ PodLens</div>
        <NavLink to="/" end>
          Dashboard
        </NavLink>
        <NavLink to="/episodes">Episodes</NavLink>
        <NavLink to="/insights">AI Insights</NavLink>
        <div className="spacer" />
        <div className="muted" style={{ fontSize: 13 }}>
          {user?.email}
        </div>
        <button onClick={logout} style={{ marginTop: 8 }}>
          Log out
        </button>
      </nav>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
