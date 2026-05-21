/**
 * Reports Page
 * Diagnosis history and report management
 */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  Calendar,
  TrendingUp,
  Eye,
  Download,
  RefreshCw,
} from "lucide-react";
import { formatDateTime, formatConfidence } from "@/utils/formatters";
import EmptyState from "@/components/common/EmptyState";
import { ROUTES } from "@/constants";
import reportApi from "@/api/reportApi";
import ErrorAlert from "@/components/common/ErrorAlert";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import ReportPdfModal from "@/components/reports/ReportPdfModal";
import { downloadBlob } from "@/utils/fileDownload";
import { useReportPdf, useToast } from "@/hooks";
import type { ReportHistoryItem } from "@/types";

const ReportsPage = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const {
    previewOpen,
    previewUrl,
    previewLoading,
    activeReportId,
    openPreview,
    closePreview,
  } = useReportPdf();

  // State for database reports
  const [dbReports, setDbReports] = useState<ReportHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoadingId, setActionLoadingId] = useState<string | null>(null);
  const [reportError, setReportError] = useState<string | null>(null);

  // Fetch reports from database on mount
  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await reportApi.getHistory({ limit: 100 });

      if (response && response.data) {
        setDbReports(response.data.history || []);
      }
    } catch (err: any) {
      toast.error("Failed to load report history.");
      setError("Failed to load report history. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleViewReport = async (report: ReportHistoryItem) => {
    if (!report.report_id) {
      toast.error("Report identifier is missing.");
      return;
    }

    try {
      setReportError(null);
      setActionLoadingId(report.report_id);
      await openPreview(report.report_id);
      toast.success("Report preview is ready.", "Preview opened");
    } catch (err) {
      toast.error("Failed to open report preview.");
      setReportError("Failed to open report preview. Please try again.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleDownloadPDF = async (report: ReportHistoryItem) => {
    try {
      setReportError(null);
      if (!report.report_id) {
        throw new Error("Report identifier is missing");
      }

      setActionLoadingId(report.report_id);
      const response = await reportApi.downloadPdf(report.report_id);
      const filename = response.filename || `${report.report_id}.pdf`;
      downloadBlob(response.data, filename, "application/pdf");
      toast.success("Report downloaded successfully.", "Download complete");
    } catch (error) {
      toast.error("Failed to download PDF report.");
      setReportError("Failed to generate PDF. Please try again.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleModalDownload = async () => {
    if (!activeReportId) {
      return;
    }

    try {
      const response = await reportApi.downloadPdf(activeReportId);
      const filename = response.filename || `${activeReportId}.pdf`;
      downloadBlob(response.data, filename, "application/pdf");
      toast.success("Report downloaded successfully.", "Download complete");
    } catch (error) {
      toast.error("Failed to download PDF report.");
    }
  };

  const handleModalPrint = () => {
    if (!previewUrl) {
      return;
    }

    const printWindow = window.open(previewUrl, "_blank");
    if (!printWindow) {
      toast.error("Unable to open print preview. Please allow popups.");
      return;
    }

    printWindow.onload = () => {
      printWindow.focus();
      printWindow.print();
    };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 flex items-center justify-center">
        <LoadingSpinner text="Loading report history..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <ErrorAlert message={error} onClose={() => setError(null)} />
          <div className="mt-4 text-center">
            <button onClick={fetchReports} className="btn btn-primary">
              <RefreshCw className="w-4 h-4 mr-2" />
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (dbReports.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Diagnosis Reports
            </h1>
            <p className="text-gray-600">
              View and manage your diagnosis history
            </p>
          </div>

          <EmptyState
            icon={FileText}
            title="No Reports Yet"
            description="You haven't completed any diagnoses yet. Start a new diagnosis to see your reports here."
            action={
              <button
                onClick={() => navigate(ROUTES.DIAGNOSIS)}
                className="btn btn-primary"
              >
                Start New Diagnosis
              </button>
            }
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Diagnosis Reports
              </h1>
              <p className="text-gray-600">
                {dbReports.length} report{dbReports.length !== 1 ? "s" : ""} in
                history
              </p>
            </div>

            <div className="flex items-center space-x-3 mt-4 md:mt-0">
              <button
                onClick={fetchReports}
                className="btn btn-outline flex items-center"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
              <button
                onClick={() => navigate(ROUTES.DIAGNOSIS)}
                className="btn btn-primary"
              >
                New Diagnosis
              </button>
            </div>
          </div>
        </div>

        {reportError && (
          <div className="mb-6">
            <ErrorAlert
              message={reportError}
              onClose={() => setReportError(null)}
            />
          </div>
        )}

        {/* Reports Grid */}
        <div className="grid gap-6">
          {dbReports.map((session) => {
            const reportData = session.report_data;
            const topPrediction =
              reportData?.diagnosis?.top_predictions?.[0] || null;
            const symptoms = reportData?.clinical_findings?.symptoms || [];
            const confidenceValue = topPrediction?.confidence ?? 0;

            return (
              <div key={session.report_id} className="card card-hover p-6">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                        <FileText className="w-6 h-6 text-primary-600" />
                      </div>

                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {topPrediction?.disease || "Diagnosis Session"}
                        </h3>

                        <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600 mb-3">
                          <span className="flex items-center">
                            <Calendar className="w-4 h-4 mr-1" />
                            {formatDateTime(session.generated_at)}
                          </span>
                          {topPrediction && (
                            <span className="flex items-center">
                              <TrendingUp className="w-4 h-4 mr-1" />
                              {formatConfidence(confidenceValue)} confidence
                            </span>
                          )}
                          <span className="inline-flex items-center px-2 py-1 rounded-md bg-blue-100 text-blue-700 text-xs font-medium">
                            {session.report_id}
                          </span>
                        </div>

                        <div className="flex flex-wrap gap-2">
                          {symptoms
                            .slice(0, 5)
                            .map((symptom: string, index: number) => (
                              <span
                                key={index}
                                className="inline-flex items-center px-2.5 py-1 rounded-md bg-gray-100 text-gray-700 text-xs font-medium"
                              >
                                {symptom}
                              </span>
                            ))}
                          {symptoms.length > 5 && (
                            <span className="inline-flex items-center px-2.5 py-1 rounded-md bg-gray-100 text-gray-600 text-xs">
                              +{symptoms.length - 5} more
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 mt-4 md:mt-0 md:ml-4">
                    <button
                      onClick={() => handleViewReport(session)}
                      className="btn btn-outline flex items-center"
                      disabled={actionLoadingId === session.report_id}
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      View Report
                    </button>
                    <button
                      onClick={() => handleDownloadPDF(session)}
                      className="btn btn-secondary flex items-center"
                      disabled={actionLoadingId === session.report_id}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      {actionLoadingId === session.report_id
                        ? "Preparing..."
                        : "Download PDF"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <ReportPdfModal
        open={previewOpen}
        pdfUrl={previewUrl}
        loading={previewLoading}
        onClose={closePreview}
        onDownload={handleModalDownload}
        onPrint={handleModalPrint}
        title="Report Preview"
      />
    </div>
  );
};

export default ReportsPage;
