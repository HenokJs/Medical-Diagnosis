/**
 * Diagnosis Card Component
 * Professional prediction display with confidence and severity
 */

import { AlertCircle, CheckCircle2, Info } from "lucide-react";
import SeverityBadge from "../common/SeverityBadge";
import ConfidenceBar from "../common/ConfidenceBar";
import type { Prediction } from "@/types";

interface DiagnosisCardProps {
  prediction: Prediction;
  rank: number;
  isTopPrediction?: boolean;
}

const DiagnosisCard = ({
  prediction,
  rank,
  isTopPrediction = false,
}: DiagnosisCardProps) => {
  const rankColors = {
    1: "border-primary-200 bg-primary-50",
    2: "border-primary-100 bg-primary-50",
    3: "border-primary-100 bg-white",
  };

  const rankBadgeColors = {
    1: "bg-primary-600 text-white",
    2: "bg-primary-500 text-white",
    3: "bg-primary-400 text-white",
  };

  return (
    <div
      className={`card p-6 ${rankColors[rank as keyof typeof rankColors] || "border-gray-200"} ${
        isTopPrediction ? "ring-2 ring-primary-500" : ""
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <span
              className={`inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold ${
                rankBadgeColors[rank as keyof typeof rankBadgeColors] ||
                "bg-primary-400 text-white"
              }`}
            >
              #{rank}
            </span>
            <h3 className="text-xl font-bold text-primary-dark">
              {prediction.disease}
            </h3>
          </div>
          <div className="flex items-center space-x-3">
            <SeverityBadge severity={prediction.severity} />
            {isTopPrediction && (
              <span className="inline-flex items-center text-xs font-medium text-primary-700">
                <CheckCircle2 className="w-4 h-4 mr-1" />
                Top Prediction
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Confidence Bar */}
      <div className="mb-4">
        <ConfidenceBar confidence={prediction.confidence} />
      </div>

      {/* Description */}
      {prediction.description && (
        <div className="mb-4">
          <div className="flex items-start space-x-2">
            <Info className="w-4 h-4 text-primary-600 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-primary-800">{prediction.description}</p>
          </div>
        </div>
      )}

      {/* Precautions */}
      {prediction.precautions && prediction.precautions.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-primary-dark mb-2 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1 text-primary-600" />
            Precautions
          </h4>
          <ul className="space-y-1">
            {prediction.precautions.slice(0, 3).map((precaution, index) => (
              <li
                key={index}
                className="text-sm text-primary-800 flex items-start"
              >
                <span className="text-primary-600 mr-2">•</span>
                <span>{precaution}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {prediction.recommendations && prediction.recommendations.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-primary-dark mb-2">
            Recommendations
          </h4>
          <ul className="space-y-1">
            {prediction.recommendations
              .slice(0, 3)
              .map((recommendation, index) => (
                <li
                  key={index}
                  className="text-sm text-primary-800 flex items-start"
                >
                  <span className="text-primary-600 mr-2">•</span>
                  <span>{recommendation}</span>
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DiagnosisCard;
