/**
 * Severity Badge Component
 * Professional severity indicator
 */

import { SEVERITY_COLORS } from "@/constants";
import { formatSeverityLabel } from "@/utils/formatters";

interface SeverityBadgeProps {
  severity: string;
  size?: "sm" | "md" | "lg";
}

const SeverityBadge = ({ severity, size = "md" }: SeverityBadgeProps) => {
  const key = severity.toLowerCase() as keyof typeof SEVERITY_COLORS;
  const colors = SEVERITY_COLORS[key] || SEVERITY_COLORS.unknown;

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-2.5 py-1",
    lg: "text-base px-3 py-1.5",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full font-medium ${colors.badge} ${sizeClasses[size]}`}
    >
      {formatSeverityLabel(severity)}
    </span>
  );
};

export default SeverityBadge;
