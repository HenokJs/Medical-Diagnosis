/**
 * Symptom Distribution Chart
 * Shows matched vs unmatched symptom counts
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

interface SymptomDistributionChartProps {
  matchedCount: number;
  unmatchedCount: number;
}

const SymptomDistributionChart = ({
  matchedCount,
  unmatchedCount,
}: SymptomDistributionChartProps) => {
  const data = [
    { name: "Matched", value: matchedCount },
    { name: "Unmatched", value: unmatchedCount },
  ];

  const colors = ["#0077b6", "#90e0ef"];

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-primary-dark mb-4">
        Symptom Distribution
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            innerRadius={50}
            outerRadius={90}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-4 flex items-center justify-center space-x-6 text-sm text-primary-700">
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-primary-600" />
          <span>Matched: {matchedCount}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-primary-100" />
          <span>Unmatched: {unmatchedCount}</span>
        </div>
      </div>
    </div>
  );
};

export default SymptomDistributionChart;
