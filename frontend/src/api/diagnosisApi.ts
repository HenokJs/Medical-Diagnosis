/**
 * Diagnosis API Service
 * All diagnosis-related API calls
 */

import apiClient from "./axios";
import type {
  ApiResponse,
  DiagnosisRequest,
  DiagnosisResponse,
  Disease,
  Symptom,
  HealthStatus,
  ModelInfo,
} from "@/types";

const requestWithFallback = async <T>(paths: string[]): Promise<T> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.get<T>(path);
      return response.data;
    } catch (error: any) {
      lastError = error;
      if (error?.response?.status === 404) {
        continue;
      }
      throw error;
    }
  }

  throw lastError || new Error("No available endpoint");
};

export const diagnosisApi = {
  /**
   * Submit diagnosis prediction request
   */
  predict: async (data: DiagnosisRequest): Promise<DiagnosisResponse> => {
    const response = await apiClient.post<DiagnosisResponse>(
      "/diagnosis/predict",
      data,
    );
    return response.data;
  },

  /**
   * Detailed symptom analysis
   */
  analyze: async (data: DiagnosisRequest): Promise<ApiResponse<any>> => {
    const response = await apiClient.post<ApiResponse<any>>(
      "/diagnosis/analyze",
      data,
    );
    return response.data;
  },

  /**
   * Batch diagnosis
   */
  batch: async (
    patients: Array<Record<string, any>>,
  ): Promise<ApiResponse<any>> => {
    const response = await apiClient.post<ApiResponse<any>>(
      "/diagnosis/batch",
      { patients },
    );
    return response.data;
  },

  /**
   * Get all available diseases
   */
  getDiseases: async (): Promise<Disease[]> => {
    const response = await requestWithFallback<
      ApiResponse<{ diseases: string[] }>
    >(["/admin/diseases", "/diseases"]);
    const list = response.data?.diseases ?? [];
    return list.map((name: string) => ({ name }));
  },

  /**
   * Get all available symptoms
   */
  getSymptoms: async (): Promise<Symptom[]> => {
    const response = await requestWithFallback<
      ApiResponse<{ symptoms: string[] }>
    >(["/admin/symptoms", "/symptoms"]);
    const list = response.data?.symptoms ?? [];
    return list.map((name: string) => ({ name }));
  },

  /**
   * Get system health status
   */
  getHealth: async (): Promise<HealthStatus> => {
    return requestWithFallback<HealthStatus>(["/health", "/health/health"]);
  },

  /**
   * Simple ping for latency checks
   */
  ping: async (): Promise<{ status: string; message: string }> => {
    return requestWithFallback<{ status: string; message: string }>([
      "/health/ping",
      "/ping",
    ]);
  },

  /**
   * Get ML model information
   */
  getModelInfo: async (): Promise<ModelInfo> => {
    const response =
      await apiClient.get<ApiResponse<ModelInfo>>("/admin/model/info");
    return response.data.data;
  },

  /**
   * Get system statistics
   */
  getStats: async (): Promise<Record<string, any>> => {
    const response =
      await apiClient.get<ApiResponse<Record<string, any>>>("/admin/stats");
    return response.data.data;
  },
};

export default diagnosisApi;
