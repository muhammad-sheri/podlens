import { useState } from "react";
import client from "../api/client.js";

export default function Insights() {
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function generate() {
    setBusy(true);
    setError("");
    try {
      const { data } = await client.post("/insights/generate");
      setResult(data);
    } catch {
      setError("Could not generate an insight.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h1>AI Insights</h1>
      <div className="panel">
        <p className="muted">
          Generate an AI summary of your podcast performance. Without an
          Anthropic API key the backend returns a clearly-labeled stub; set the
          key to enable live Claude analysis.
        </p>
        <button onClick={generate} disabled={busy}>
          {busy ? "Analyzing…" : "Generate insight"}
        </button>
        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
        {result && (
          <>
            <div className="muted" style={{ marginTop: 16, fontSize: 12 }}>
              source: {result.source}
            </div>
            <div className="insight">{result.text}</div>
          </>
        )}
      </div>
    </div>
  );
}
