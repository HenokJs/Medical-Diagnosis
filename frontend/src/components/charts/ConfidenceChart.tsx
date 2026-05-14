/**
 * Confidence Comparison Chart
 * Professional bar chart using Recharts
 */

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { Prediction } from "@/types";

interface ConfidenceChartProps {
  predictions: Prediction[];
}

const ConfidenceChart = ({ predictions }: ConfidenceChartProps) => {
  const data = predictions.slice(0, 3).map((pred, index) => ({
    name: pred.disease,
    confidence: pred.confidence * 100,
    rank: index + 1,
  }));

  const colors = ["#0077b6", "#00b4d8", "#90e0ef"];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-primary-200">
          <p className="font-semibold text-primary-dark">
            {payload[0].payload.name}
          </p>
          <p className="text-sm text-primary-700">
            Confidence:{" "}
            <span className="font-medium">{payload[0].value.toFixed(1)}%</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-primary-dark mb-4">
        Confidence Comparison
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#90e0ef" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={100}
            tick={{ fill: "#03045e", fontSize: 12 }}
          />
          <YAxis
            label={{
              value: "Confidence (%)",
              angle: -90,
              position: "insideLeft",
              fill: "#03045e",
            }}
            tick={{ fill: "#03045e", fontSize: 12 }}
            domain={[0, 100]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="confidence" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConfidenceChart;
