/**
 * Report API Service
 * Report generation and retrieval
 */

import apiClient from "./axios";
import type {
  ReportHistoryResponse,
  ReportRequest,
  ReportResponse,
} from "@/types";
import { getFilenameFromDisposition } from "@/utils/fileDownload";

const postJsonWithFallback = async <T>(
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

const postBlobWithFallback = async (
  paths: string[],
  payload: ReportRequest,
): Promise<{ data: Blob; filename?: string }> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.post<Blob>(path, payload, {
        responseType: "blob",
      });
      return {
        data: response.data,
        filename: getFilenameFromDisposition(
          response.headers["content-disposition"],
        ),
      };
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
  params?: any,
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

const getBlobWithFallback = async (
  paths: string[],
  params?: any,
): Promise<{ data: Blob; filename?: string }> => {
  let lastError: unknown = null;

  for (const path of paths) {
    try {
      const response = await apiClient.get<Blob>(path, {
        params,
        responseType: "blob",
      });
      return {
        data: response.data,
        filename: getFilenameFromDisposition(
          response.headers["content-disposition"],
        ),
      };
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
    return postJsonWithFallback<ReportResponse>(
      ["/report/generate", "/reports/generate"],
      payload,
    );
  },

  /**
   * Generate PDF directly from payload
   */
  generatePdf: async (
    payload: ReportRequest,
  ): Promise<{ data: Blob; filename?: string }> => {
    return postBlobWithFallback(["/report/generate", "/reports/generate"], {
      ...payload,
      format: "pdf",
    });
  },

  /**
   * Get report history from database
   */
  getHistory: async (params?: {
    patient_id?: string;
    page?: number;
    limit?: number;
  }) => {
    return getWithFallback<ReportHistoryResponse>(
      ["/report/history", "/reports/history"],
      params,
    );
  },

  /**
   * Get report data by report id
   */
  getById: async (reportId: string) => {
    return getWithFallback<ReportResponse>([
      "/report/" + reportId,
      "/reports/" + reportId,
    ]);
  },

  /**
   * Download PDF by report id
   */
  downloadPdf: async (
    reportId: string,
  ): Promise<{ data: Blob; filename?: string }> => {
    return getBlobWithFallback([
      "/report/" + reportId + "/pdf",
      "/reports/" + reportId + "/pdf",
    ]);
  },
};

export default reportApi;
