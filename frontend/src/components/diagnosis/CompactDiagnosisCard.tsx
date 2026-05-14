/**
 * Compact Diagnosis Card - Refined Design
 * Professional, space-efficient, modern healthcare UI
 */

import { useState } from 'react';
import { ChevronDown, ChevronUp, AlertCircle, Info } from 'lucide-react';
import SeverityBadge from '../common/SeverityBadge';
import { formatConfidence } from '@/utils/formatters';
import type { Prediction } from '@/types';

interface CompactDiagnosisCardProps {
  prediction: Prediction;
  rank: number;
  isTopPrediction?: boolean;
}

const CompactDiagnosisCard = ({
  prediction,
  rank,
  isTopPrediction = false,
}: CompactDiagnosisCardProps) => {
  const [isExpanded, setIsExpanded] = useState(rank === 1);

  const rankColors = {
    1: 'from-primary-500 to-primary-600',
    2: 'from-blue-500 to-blue-600',
    3: 'from-gray-500 to-gray-600',
  };

  const confidence = prediction.confidence * 100;

  return (
    <div
      className={`card overflow-hidden transition-all ${
        isTopPrediction ? 'ring-2 ring-primary-400 shadow-md' : ''
      }`}
    >
      {/* Header - Always Visible */}
      <div className="p-4">
        <div className="flex items-start justify-between gap-4">
          {/* Left: Rank & Disease */}
          <div className="flex items-start gap-3 flex-1 min-w-0">
            {/* Rank Badge */}
            <div
              className={`flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br ${
                rankColors[rank as keyof typeof rankColors] || 'from-gray-500 to-gray-600'
              } flex items-center justify-center shadow-sm`}
            >
              <span className="text-lg font-bold text-white">#{rank}</span>
            </div>

            {/* Disease Info */}
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-bold text-gray-900 mb-1 truncate">
                {prediction.disease}
              </h3>
              <div className="flex items-center gap-2 flex-wrap">
                <SeverityBadge severity={prediction.severity} size="sm" />
                {isTopPrediction && (
                  <span className="text-xs font-medium text-primary-700 bg-primary-50 px-2 py-0.5 rounded">
                    Top Match
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Right: Confidence */}
          <div className="flex-shrink-0 text-right">
            <div className="text-2xl font-bold text-gray-900">
              {confidence.toFixed(1)}%
            </div>
            <div className="text-xs text-gray-500">confidence</div>
          </div>
        </div>

        {/* Confidence Bar */}
        <div className="mt-3">
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div
              className={`h-full bg-gradient-to-r ${
                confidence >= 80
                  ? 'from-green-500 to-green-600'
                  : confidence >= 60
                  ? 'from-blue-500 to-blue-600'
                  : confidence >= 40
                  ? 'from-amber-500 to-amber-600'
                  : 'from-red-500 to-red-600'
              } transition-all duration-500 ease-out`}
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>

        {/* Description - Compact */}
        {prediction.description && (
          <p className="mt-3 text-sm text-gray-600 line-clamp-2">
            {prediction.description}
          </p>
        )}

        {/* Expand/Collapse Button */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-3 w-full flex items-center justify-center gap-2 text-sm font-medium text-primary-600 hover:text-primary-700 py-2 hover:bg-primary-50 rounded-lg transition-colors"
        >
          {isExpanded ? (
            <>
              <span>Show Less</span>
              <ChevronUp className="w-4 h-4" />
            </>
          ) : (
            <>
              <span>Show Details</span>
              <ChevronDown className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="border-t border-gray-100 bg-gray-50 p-4 space-y-4">
          {/* Precautions */}
          {prediction.precautions && prediction.precautions.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-4 h-4 text-amber-600" />
                <h4 className="text-sm font-semibold text-gray-900">Precautions</h4>
              </div>
              <ul className="space-y-1.5">
                {prediction.precautions.slice(0, 4).map((precaution, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-amber-600 mt-1">•</span>
                    <span className="flex-1">{precaution}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {prediction.recommendations && prediction.recommendations.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Info className="w-4 h-4 text-blue-600" />
                <h4 className="text-sm font-semibold text-gray-900">Recommendations</h4>
              </div>
              <ul className="space-y-1.5">
                {prediction.recommendations.slice(0, 4).map((recommendation, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-blue-600 mt-1">•</span>
                    <span className="flex-1">{recommendation}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CompactDiagnosisCard;
