/**
 * Report API Service
 * Report generation and retrieval
 */

import apiClient from "./axios";
import type { ReportRequest, ReportResponse } from "@/types";

const postWithFallback = async <T>(
  paths: string[],
  payload: ReportRequest,
): Promise<T> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.post<T>(path, payload);
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
    return postWithFallback<ReportResponse>(
      ["/report/generate", "/reports/generate"],
      payload,
    );
  },
};

export default reportApi;
