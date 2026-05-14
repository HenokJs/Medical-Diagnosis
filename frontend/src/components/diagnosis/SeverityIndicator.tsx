/**
 * Severity Indicator
 * Shows overall severity and risk level
 */

import SeverityBadge from "@/components/common/SeverityBadge";
import { formatRiskLevel } from "@/utils/formatters";

interface SeverityIndicatorProps {
  severity: string;
  riskLevel: string;
  symptomsProcessed?: number;
  symptomsMatched?: number;
}

const SeverityIndicator = ({
  severity,
  riskLevel,
  symptomsProcessed,
  symptomsMatched,
}: SeverityIndicatorProps) => {
  const matchRate =
    symptomsProcessed && symptomsProcessed > 0
      ? Math.round(((symptomsMatched || 0) / symptomsProcessed) * 100)
      : undefined;

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Severity Overview
      </h3>
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-sm text-gray-600 mb-2">Overall Severity</p>
          <SeverityBadge severity={severity} size="lg" />
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600 mb-2">Risk Level</p>
          <p className="text-lg font-semibold text-gray-900">
            {formatRiskLevel(riskLevel)}
          </p>
        </div>
      </div>

      {matchRate !== undefined && (
        <div>
          <p className="text-sm text-gray-600 mb-2">Symptom Match Rate</p>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="h-2 rounded-full bg-primary-600"
              style={{ width: `${matchRate}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {symptomsMatched || 0} of {symptomsProcessed} symptoms matched
          </p>
        </div>
      )}
    </div>
  );
};

export default SeverityIndicator;
