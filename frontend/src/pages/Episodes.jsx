import { useEffect, useState } from "react";
import client from "../api/client.js";

export default function Episodes() {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    client
      .get("/analytics/episodes")
      .then((r) => setRows(r.data))
      .catch(() => setError("Could not load episodes."));
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!rows) return <div>Loading episodes…</div>;

  const fmt = (n) => n.toLocaleString();

  return (
    <div>
      <h1>Episodes</h1>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Episode</th>
              <th>Downloads</th>
              <th>Listeners</th>
              <th>Avg retention</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.episode_id}>
                <td>{row.title}</td>
                <td>{fmt(row.downloads)}</td>
                <td>{fmt(row.listeners)}</td>
                <td>{row.avg_retention}%</td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && (
          <p className="muted">No episode data yet. Run the seed command.</p>
        )}
      </div>
    </div>
  );
}
