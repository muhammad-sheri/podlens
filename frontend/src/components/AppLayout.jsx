import { NavLink, Outlet } from "react-router-dom";

export default function AppLayout() {
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
        <div className="nav-footer">Podcast analytics</div>
      </nav>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
