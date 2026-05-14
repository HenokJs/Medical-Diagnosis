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
  // Null safety check
  if (!predictions || predictions.length === 0) {
    return (
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-primary-dark mb-4">
          Prediction Ranking
        </h3>
        <div className="flex items-center justify-center h-64 text-neutral-500">
          <p className="text-sm">No prediction data available</p>
        </div>
      </div>
    );
  }

  const data = predictions.slice(0, 5).map((pred) => ({
    name: pred?.disease || pred?.disease_name || "Unknown",
    confidence: (pred?.confidence || pred?.confidence_score || 0) * 100,
  }));

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
        Prediction Ranking
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 20, left: 20, bottom: 10 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#90e0ef" />
          <XAxis
            type="number"
            domain={[0, 100]}
            tick={{ fill: "#03045e", fontSize: 12 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={140}
            tick={{ fill: "#03045e", fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="confidence" fill="#0077b6" radius={[0, 8, 8, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionRankingChart;
