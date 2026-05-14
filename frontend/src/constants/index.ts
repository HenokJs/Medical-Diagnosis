/**
 * Application Constants
 */

export const APP_NAME = "MedAI Diagnosis";
export const APP_VERSION = "1.0.0";

export const SEVERITY_COLORS = {
  minor: {
    bg: "bg-green-50",
    text: "text-green-700",
    border: "border-green-200",
    badge: "bg-green-100 text-green-800",
  },
  moderate: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    border: "border-amber-200",
    badge: "bg-amber-100 text-amber-800",
  },
  urgent: {
    bg: "bg-red-50",
    text: "text-red-700",
    border: "border-red-200",
    badge: "bg-red-100 text-red-800",
  },
  critical: {
    bg: "bg-red-100",
    text: "text-red-900",
    border: "border-red-300",
    badge: "bg-red-200 text-red-900",
  },
  unknown: {
    bg: "bg-gray-50",
    text: "text-gray-700",
    border: "border-gray-200",
    badge: "bg-gray-100 text-gray-800",
  },
} as const;

export const MEDICAL_DISCLAIMER =
  "This AI-powered system provides diagnostic suggestions for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.";

export const SYMPTOM_CATEGORIES = [
  "General",
  "Respiratory",
  "Cardiovascular",
  "Gastrointestinal",
  "Neurological",
  "Musculoskeletal",
  "Dermatological",
  "Other",
] as const;

export const ROUTES = {
  HOME: "/",
  DIAGNOSIS: "/diagnosis",
  RESULTS: "/results",
  REPORTS: "/reports",
  STATUS: "/status",
} as const;

export const API_ENDPOINTS = {
  PREDICT: "/diagnosis/predict",
  ANALYZE: "/diagnosis/analyze",
  BATCH: "/diagnosis/batch",
  REPORT: "/report/generate",
  DISEASES: "/admin/diseases",
  SYMPTOMS: "/admin/symptoms",
  HEALTH: "/health",
  PING: "/health/ping",
  MODEL_INFO: "/admin/model/info",
  STATS: "/admin/stats",
} as const;
