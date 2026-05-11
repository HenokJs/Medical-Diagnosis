/**
 * Prediction Ranking Chart
 * Horizontal bar chart for top predictions
 */

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { Prediction } from "@/types";

interface PredictionRankingChartProps {
  predictions: Prediction[];
}

const PredictionRankingChart = ({
  predictions,
}: PredictionRankingChartProps) => {
  const data = predictions.slice(0, 5).map((pred) => ({
    name: pred.disease,
    confidence: pred.confidence * 100,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-900">
            {payload[0].payload.name}
          </p>
          <p className="text-sm text-gray-600">
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
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Prediction Ranking
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 20, left: 20, bottom: 10 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            type="number"
            domain={[0, 100]}
            tick={{ fill: "#6b7280", fontSize: 12 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={140}
            tick={{ fill: "#6b7280", fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="confidence" fill="#2563eb" radius={[0, 8, 8, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionRankingChart;
