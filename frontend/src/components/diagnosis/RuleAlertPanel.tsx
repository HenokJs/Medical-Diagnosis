/**
 * Rule Engine Alert Panel
 * Professional display of clinical validation alerts
 */

import { AlertTriangle, Info, AlertCircle } from "lucide-react";
import type { RuleEngineFlag } from "@/types";

interface RuleAlertPanelProps {
  alerts: RuleEngineFlag[];
}

const RuleAlertPanel = ({ alerts }: RuleAlertPanelProps) => {
  if (!alerts || alerts.length === 0) {
    return null;
  }

  const getAlertIcon = (priority: string) => {
    switch (priority) {
      case "critical":
        return <AlertCircle className="w-5 h-5" />;
      case "high":
        return <AlertTriangle className="w-5 h-5" />;
      case "medium":
        return <AlertTriangle className="w-5 h-5" />;
      default:
        return <Info className="w-5 h-5" />;
    }
  };

  const getAlertStyles = (priority: string) => {
    switch (priority) {
      case "critical":
        return "bg-red-50 border-red-200 text-red-800";
      case "high":
        return "bg-amber-50 border-amber-200 text-amber-800";
      case "medium":
        return "bg-blue-50 border-blue-200 text-blue-800";
      default:
        return "bg-gray-50 border-gray-200 text-gray-800";
    }
  };

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Clinical Validation Alerts
      </h3>
      <div className="space-y-3">
        {alerts.map((alert, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg border flex items-start space-x-3 ${getAlertStyles(
              alert.priority,
            )}`}
          >
            <div className="flex-shrink-0 mt-0.5">
              {getAlertIcon(alert.priority)}
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-xs font-semibold uppercase tracking-wide">
                  {alert.category}
                </span>
                <span className="text-xs font-medium">• {alert.priority}</span>
              </div>
              <p className="text-sm font-medium">{alert.name}</p>
              <p className="text-sm opacity-90 mt-1">{alert.explanation}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RuleAlertPanel;
