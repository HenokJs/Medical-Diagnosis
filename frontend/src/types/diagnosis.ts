/**
 * Core TypeScript Types for Medical Diagnosis System
 * Matches Flask backend API responses
 */

export type SeverityLevel =
  | "minor"
  | "moderate"
  | "urgent"
  | "critical"
  | "unknown";

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  timestamp: string;
  error_code?: string;
  details?: unknown;
}

export interface PatientInfo {
  age: number;
  gender: "male" | "female" | "other" | "unknown";
  symptomDuration?: string;
  notes?: string;
  name?: string;
  patient_id?: string;
}

export interface DiagnosisRequest {
  symptoms: string[];
  age?: number;
  gender?: string;
  duration_days?: number;
  free_text?: string;
}

export interface Prediction {
  disease: string;
  confidence: number;
  confidence_percent?: string;
  severity: SeverityLevel;
  description?: string;
  precautions?: string[];
  recommendations?: string[];
}

export interface ExplainabilityFeature {
  symptom: string;
  importance: number;
}

export interface Explainability {
  matched_symptoms: string[];
  unmatched_symptoms?: string[];
  important_features: ExplainabilityFeature[];
  confidence_reasoning?: string;
  prediction_factors?: string[];
}

export interface RuleEngineFlag {
  rule_id: string;
  name: string;
  action: string;
  priority: "low" | "medium" | "high" | "critical";
  category: string;
  explanation: string;
  triggered_by?: string[];
}

export interface PatientAnalysis {
  severity: SeverityLevel;
  risk_level: "low" | "medium" | "high" | "critical" | "unknown";
  symptoms_processed?: number;
  symptoms_matched?: number;
  age?: number;
  gender?: string;
  duration_days?: number;
}

export interface DiagnosisData {
  success: boolean;
  patient_analysis: PatientAnalysis;
  top_predictions: Prediction[];
  explainability: Explainability;
  rule_engine_flags: RuleEngineFlag[];
  recommendation?: string;
  disclaimer?: string;
}

export type DiagnosisResponse = ApiResponse<DiagnosisData>;

export interface Disease {
  name: string;
  category?: string;
  severity?: string;
}

export interface Symptom {
  name: string;
  category?: string;
  common?: boolean;
}

export interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy";
  models_loaded: boolean;
  uptime: string;
  version: string;
  environment?: string;
  debug?: boolean;
  timestamp: string;
}

export interface ModelInfo {
  model_type: string;
  num_features: number;
  num_diseases: number;
  loaded: boolean;
  best_model?: string;
  accuracy?: number;
  top3_accuracy?: number;
  training_date?: string;
}

export interface DiagnosisHistory {
  id: string;
  timestamp: string;
  symptoms: string[];
  topPrediction: string;
  confidence: number;
  diagnosis: DiagnosisResponse;
  patientInfo?: PatientInfo;
}

export interface ReportRequest {
  diagnosis_result: DiagnosisData;
  patient_info: PatientInfo;
  format?: "json" | "html" | "pdf";
}

export interface ReportData {
  report_id: string;
  generated_at: string;
  patient_info: PatientInfo;
  diagnosis: {
    top_predictions: Prediction[];
    severity: SeverityLevel;
    risk_level: string;
  };
  clinical_findings: {
    symptoms: string[];
    rule_flags: RuleEngineFlag[];
  };
  recommendation?: string;
  disclaimer?: string;
  report_path?: string;
}

export type ReportResponse = ApiResponse<ReportData>;
