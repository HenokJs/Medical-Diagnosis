/**
 * Explainability Panel Component
 * Shows AI reasoning and matched symptoms
 */

import { Brain, CheckCircle, TrendingUp, AlertCircle } from "lucide-react";
import type { Explainability } from "@/types";

interface ExplainabilityPanelProps {
  explainability: Explainability;
}

const ExplainabilityPanel = ({ explainability }: ExplainabilityPanelProps) => {
  return (
    <div className="card p-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
          <Brain className="w-6 h-6 text-purple-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            AI Explainability
          </h3>
          <p className="text-sm text-gray-600">
            Understanding the diagnosis reasoning
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Matched Symptoms */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h4 className="text-sm font-semibold text-gray-900">
              Matched Symptoms ({explainability.matched_symptoms.length})
            </h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {explainability.matched_symptoms.map((symptom, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1.5 rounded-lg bg-green-50 text-green-700 text-sm font-medium border border-green-200"
              >
                {symptom}
              </span>
            ))}
          </div>
        </div>

        {/* Important Features */}
        {explainability.important_features.length > 0 && (
          <div>
            <div className="flex items-center space-x-2 mb-3">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              <h4 className="text-sm font-semibold text-gray-900">
                Key Diagnostic Features (
                {explainability.important_features.length})
              </h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {explainability.important_features
                .slice(0, 10)
                .map((feature, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 text-sm font-medium border border-blue-200"
                  >
                    {feature.symptom}
                    <span className="ml-2 text-xs text-blue-600">
                      {(feature.importance * 100).toFixed(1)}%
                    </span>
                  </span>
                ))}
            </div>
          </div>
        )}

        {/* Confidence Reasoning */}
        {explainability.confidence_reasoning && (
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <h4 className="text-sm font-semibold text-gray-900 mb-2">
              Confidence Reasoning
            </h4>
            <p className="text-sm text-gray-700 leading-relaxed">
              {explainability.confidence_reasoning}
            </p>
          </div>
        )}

        {/* Prediction Factors */}
        {explainability.prediction_factors &&
          explainability.prediction_factors.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-3">
                Prediction Factors
              </h4>
              <div className="space-y-2">
                {explainability.prediction_factors
                  .slice(0, 5)
                  .map((factor, index) => (
                    <div
                      key={index}
                      className="flex items-start space-x-2 text-sm text-gray-700"
                    >
                      <AlertCircle className="w-4 h-4 text-gray-500 mt-0.5" />
                      <span>{factor}</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

        {/* Unmatched Symptoms */}
        {explainability.unmatched_symptoms &&
          explainability.unmatched_symptoms.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-3">
                Unmatched Symptoms ({explainability.unmatched_symptoms.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {explainability.unmatched_symptoms
                  .slice(0, 8)
                  .map((symptom, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-1.5 rounded-lg bg-gray-100 text-gray-700 text-sm font-medium border border-gray-200"
                    >
                      {symptom}
                    </span>
                  ))}
              </div>
            </div>
          )}
      </div>
    </div>
  );
};

export default ExplainabilityPanel;
