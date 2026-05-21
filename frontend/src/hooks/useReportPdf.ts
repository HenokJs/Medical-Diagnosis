/**
 * Report PDF helper hook
 */

import { useState } from "react";
import reportApi from "@/api/reportApi";
import { createBlobUrl, revokeBlobUrl } from "@/utils/fileDownload";

export const useReportPdf = () => {
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeReportId, setActiveReportId] = useState<string | null>(null);

  const closePreview = () => {
    revokeBlobUrl(previewUrl);
    setPreviewUrl(null);
    setPreviewOpen(false);
    setActiveReportId(null);
  };

  const openPreview = async (reportId: string) => {
    setLoading(true);
    try {
      revokeBlobUrl(previewUrl);
      const response = await reportApi.downloadPdf(reportId);
      const url = createBlobUrl(response.data);
      setPreviewUrl(url);
      setPreviewOpen(true);
      setActiveReportId(reportId);
      return response;
    } finally {
      setLoading(false);
    }
  };

  const refreshPreview = async () => {
    if (!activeReportId) {
      return null;
    }
    closePreview();
    return openPreview(activeReportId);
  };

  return {
    activeReportId,
    previewOpen,
    previewUrl,
    previewLoading: loading,
    openPreview,
    closePreview,
    refreshPreview,
    setPreviewOpen,
  };
};
