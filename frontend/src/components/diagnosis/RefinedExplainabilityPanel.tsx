/**
 * Refined Explainability Panel
 * Clean, professional AI reasoning display
 */

import { Brain, CheckCircle, TrendingUp, Lightbulb } from 'lucide-react';
import type { Explainability } from '@/types';

interface RefinedExplainabilityPanelProps {
  explainability: Explainability;
}

const RefinedExplainabilityPanel = ({ explainability }: RefinedExplainabilityPanelProps) => {
  return (
    <div className="card p-5">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center shadow-sm">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-base font-semibold text-gray-900">AI Explainability</h3>
          <p className="text-xs text-gray-600">Understanding the diagnosis reasoning</p>
        </div>
      </div>

      <div className="space-y-4">
        {/* Matched Symptoms */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <h4 className="text-sm font-semibold text-gray-900">
              Matched Symptoms ({explainability.matched_symptoms.length})
            </h4>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {explainability.matched_symptoms.map((symptom, index) => (
              <span
                key={index}
                className="inline-flex items-center px-2.5 py-1 rounded-md bg-green-50 text-green-700 text-xs font-medium border border-green-200"
              >
                {symptom}
              </span>
            ))}
          </div>
        </div>

        {/* Important Features */}
        {explainability.important_features.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-blue-600" />
              <h4 className="text-sm font-semibold text-gray-900">
                Key Diagnostic Features
              </h4>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {explainability.important_features.slice(0, 8).map((feature, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-medium border border-blue-200"
                >
                  {feature}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Reasoning */}
        {explainability.reasoning && (
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-3 border border-gray-200">
            <div className="flex items-start gap-2">
              <Lightbulb className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-semibold text-gray-900 mb-1">Clinical Reasoning</h4>
                <p className="text-sm text-gray-700 leading-relaxed">{explainability.reasoning}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RefinedExplainabilityPanel;
