/**
 * Utility Functions for Formatting
 */

/**
 * Format confidence score as percentage
 */
export const formatConfidence = (confidence: number): string => {
  return `${(confidence * 100).toFixed(1)}%`;
};

/**
 * Format date/time
 */
export const formatDateTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

/**
 * Format processing time
 */
export const formatProcessingTime = (time: string): string => {
  const seconds = parseFloat(time.replace("s", ""));
  if (seconds < 1) {
    return `${(seconds * 1000).toFixed(0)}ms`;
  }
  return `${seconds.toFixed(2)}s`;
};

/**
 * Capitalize first letter
 */
export const capitalize = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Get severity color class
 */
export const getSeverityColor = (severity: string): string => {
  const colors: Record<string, string> = {
    minor: "text-green-600",
    moderate: "text-amber-600",
    urgent: "text-red-600",
    critical: "text-red-900",
    unknown: "text-gray-600",
  };
  const key = severity.toLowerCase();
  return colors[key] || "text-gray-600";
};

/**
 * Get confidence level label
 */
export const getConfidenceLevel = (confidence: number): string => {
  if (confidence >= 0.9) return "Very High";
  if (confidence >= 0.75) return "High";
  if (confidence >= 0.6) return "Moderate";
  if (confidence >= 0.4) return "Low";
  return "Very Low";
};

/**
 * Format severity label for display
 */
export const formatSeverityLabel = (severity: string): string => {
  const normalized = severity.toLowerCase();
  if (normalized === "unknown") return "Unknown";
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
};

/**
 * Format risk level label for display
 */
export const formatRiskLevel = (risk: string): string => {
  const normalized = risk.toLowerCase();
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
};

/**
 * Parse a duration string into days if possible
 */
export const parseDurationDays = (input: string): number | undefined => {
  if (!input) return undefined;
  const trimmed = input.trim().toLowerCase();
  const match = trimmed.match(/(\d+(?:\.\d+)?)/);
  if (!match) return undefined;

  const value = parseFloat(match[1]);
  if (Number.isNaN(value)) return undefined;

  if (trimmed.includes("week")) return Math.round(value * 7);
  if (trimmed.includes("month")) return Math.round(value * 30);
  if (trimmed.includes("year")) return Math.round(value * 365);
  return Math.round(value);
};

/**
 * Truncate text
 */
export const truncate = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "...";
};
