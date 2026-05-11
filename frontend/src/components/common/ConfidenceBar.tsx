/**
 * Confidence Progress Bar
 * Professional confidence visualization
 */

import { formatConfidence } from '@/utils/formatters';

interface ConfidenceBarProps {
  confidence: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const ConfidenceBar = ({ confidence, showLabel = true, size = 'md' }: ConfidenceBarProps) => {
  const percentage = confidence * 100;
  
  const getColor = () => {
    if (confidence >= 0.8) return 'bg-green-500';
    if (confidence >= 0.6) return 'bg-blue-500';
    if (confidence >= 0.4) return 'bg-amber-500';
    return 'bg-red-500';
  };

  const heightClasses = {
    sm: 'h-1.5',
    md: 'h-2',
    lg: 'h-3',
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs font-medium text-gray-600">Confidence</span>
          <span className="text-xs font-semibold text-gray-900">
            {formatConfidence(confidence)}
          </span>
        </div>
      )}
      <div className={`w-full bg-gray-200 rounded-full overflow-hidden ${heightClasses[size]}`}>
        <div
          className={`${getColor()} ${heightClasses[size]} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ConfidenceBar;
