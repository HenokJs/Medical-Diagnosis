/**
 * Refined Alert Panel
 * Professional clinical validation alerts
 */

import { AlertTriangle, Info, AlertCircle, Shield } from 'lucide-react';
import type { RuleEngineAlert } from '@/types';

interface RefinedAlertPanelProps {
  alerts: RuleEngineAlert[];
}

const RefinedAlertPanel = ({ alerts }: RefinedAlertPanelProps) => {
  if (!alerts || alerts.length === 0) {
    return null;
  }

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'critical':
        return <AlertCircle className="w-5 h-5" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5" />;
      default:
        return <Info className="w-5 h-5" />;
    }
  };

  const getAlertStyles = (type: string) => {
    switch (type) {
      case 'critical':
        return {
          container: 'bg-red-50 border-red-200',
          icon: 'text-red-600',
          text: 'text-red-900',
          badge: 'bg-red-100 text-red-800',
        };
      case 'warning':
        return {
          container: 'bg-amber-50 border-amber-200',
          icon: 'text-amber-600',
          text: 'text-amber-900',
          badge: 'bg-amber-100 text-amber-800',
        };
      default:
        return {
          container: 'bg-blue-50 border-blue-200',
          icon: 'text-blue-600',
          text: 'text-blue-900',
          badge: 'bg-blue-100 text-blue-800',
        };
    }
  };

  return (
    <div className="card p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center shadow-sm">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-base font-semibold text-gray-900">Clinical Validation</h3>
          <p className="text-xs text-gray-600">{alerts.length} alert{alerts.length !== 1 ? 's' : ''} detected</p>
        </div>
      </div>

      <div className="space-y-2.5">
        {alerts.map((alert, index) => {
          const styles = getAlertStyles(alert.type);
          return (
            <div
              key={index}
              className={`p-3 rounded-lg border ${styles.container} flex items-start gap-3`}
            >
              <div className={`flex-shrink-0 ${styles.icon}`}>
                {getAlertIcon(alert.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-xs font-semibold uppercase tracking-wide ${styles.badge} px-2 py-0.5 rounded`}>
                    {alert.category}
                  </span>
                </div>
                <p className={`text-sm font-medium ${styles.text}`}>{alert.message}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RefinedAlertPanel;
