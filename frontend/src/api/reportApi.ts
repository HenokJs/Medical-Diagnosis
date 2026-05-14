/**
 * Report API Service
 * Report generation and retrieval
 */

import apiClient from "./axios";
import type { ReportRequest, ReportResponse } from "@/types";

const postWithFallback = async <T>(
  paths: string[],
  payload: ReportRequest,
  responseType?: 'json' | 'blob'
): Promise<T> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.post<T>(path, payload, {
        responseType: responseType || 'json'
      });
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

const getWithFallback = async <T>(
  paths: string[],
  params?: any
): Promise<T> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.get<T>(path, { params });
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

export const reportApi = {
  /**
   * Generate a clinical report
   */
  generate: async (payload: ReportRequest): Promise<ReportResponse> => {
    // If PDF format requested, expect blob response
    const responseType = payload.format === 'pdf' ? 'blob' : 'json';
    return postWithFallback<ReportResponse>(
      ["/report/generate", "/reports/generate"],
      payload,
      responseType
    );
  },

  /**
   * Get report history from database
   */
  getHistory: async (params?: { patient_id?: string; page?: number; limit?: number }) => {
    return getWithFallback<any>(
      ["/report/history", "/reports/history"],
      params
    );
  },
};

export default reportApi;
