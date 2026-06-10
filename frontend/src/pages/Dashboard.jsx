import { useEffect, useState } from "react";
import client from "../api/client.js";
import { DownloadsLineChart, PlatformBarChart } from "../components/Charts.jsx";

function StatCard({ label, value }) {
  return (
    <div className="card">
      <div className="label">{label}</div>
      <div className="value">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [platforms, setPlatforms] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      client.get("/analytics/overview"),
      client.get("/analytics/platforms"),
    ])
      .then(([o, p]) => {
        setOverview(o.data);
        setPlatforms(p.data);
      })
      .catch(() => setError("Could not load analytics."));
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!overview) return <div>Loading analytics…</div>;

  const { totals, series } = overview;
  const fmt = (n) => n.toLocaleString();

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="cards">
        <StatCard label="Downloads (90d)" value={fmt(totals.downloads)} />
        <StatCard label="Listeners (90d)" value={fmt(totals.listeners)} />
        <StatCard label="Avg retention" value={`${totals.avg_retention}%`} />
      </div>

      <div className="panel">
        <h2>Downloads &amp; listeners over time</h2>
        <DownloadsLineChart data={series} />
      </div>

      <div className="panel">
        <h2>By platform</h2>
        <PlatformBarChart data={platforms} />
      </div>
    </div>
  );
}
