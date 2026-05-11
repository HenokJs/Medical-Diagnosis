/**
 * Professional Error Alert Component
 */

import { AlertCircle, X } from 'lucide-react';

interface ErrorAlertProps {
  message: string;
  onClose?: () => void;
}

const ErrorAlert = ({ message, onClose }: ErrorAlertProps) => {
  return (
    <div className="alert alert-error flex items-start justify-between">
      <div className="flex items-start space-x-3">
        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-medium mb-1">Error</h4>
          <p className="text-sm">{message}</p>
        </div>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-red-600 hover:text-red-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};

export default ErrorAlert;
