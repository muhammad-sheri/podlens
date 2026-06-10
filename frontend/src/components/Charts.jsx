import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const AXIS = { stroke: "#9aa3b2", fontSize: 12 };
const GRID = "#2a2f3a";

export function DownloadsLineChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={AXIS} minTickGap={32} />
        <YAxis tick={AXIS} />
        <Tooltip
          contentStyle={{ background: "#1a1d24", border: "1px solid #2a2f3a" }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="downloads"
          stroke="#6c8cff"
          strokeWidth={2}
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="listeners"
          stroke="#46d29a"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function PlatformBarChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="3 3" />
        <XAxis dataKey="platform" tick={AXIS} />
        <YAxis tick={AXIS} />
        <Tooltip
          contentStyle={{ background: "#1a1d24", border: "1px solid #2a2f3a" }}
        />
        <Legend />
        <Bar dataKey="downloads" fill="#6c8cff" radius={[4, 4, 0, 0]} />
        <Bar dataKey="listeners" fill="#46d29a" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
