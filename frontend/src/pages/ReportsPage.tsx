/**
 * Reports Page
 * Diagnosis history and report management
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  Calendar,
  TrendingUp,
  Trash2,
  Eye,
  Download,
} from "lucide-react";
import { useDiagnosisStore } from "@/store/diagnosisStore";
import { formatDateTime, formatConfidence } from "@/utils/formatters";
import EmptyState from "@/components/common/EmptyState";
import { ROUTES } from "@/constants";
import reportApi from "@/api/reportApi";
import ReportViewer from "@/components/reports/ReportViewer";
import ErrorAlert from "@/components/common/ErrorAlert";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import type { ReportData } from "@/types";

const ReportsPage = () => {
  const navigate = useNavigate();
  const { diagnosisHistory, clearHistory, setCurrentDiagnosis } =
    useDiagnosisStore();
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [activeReport, setActiveReport] = useState<ReportData | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState<string | null>(null);

  const handleClearHistory = () => {
    clearHistory();
    setShowClearConfirm(false);
  };

  const handleGenerateReport = async (reportId: string) => {
    const entry = diagnosisHistory.find((item) => item.id === reportId);
    if (!entry) return;

    if (!entry.patientInfo) {
      setReportError("Patient information is required to generate a report.");
      return;
    }

    try {
      setReportError(null);
      setReportLoading(true);
      const response = await reportApi.generate({
        diagnosis_result: entry.diagnosis.data,
        patient_info: entry.patientInfo,
        format: "json",
      });
      setActiveReport(response.data);
    } catch (error) {
      setReportError("Failed to generate report. Please try again.");
    } finally {
      setReportLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!activeReport) return;
    const blob = new Blob([JSON.stringify(activeReport, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${activeReport.report_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  if (diagnosisHistory.length === 0) {
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
                {diagnosisHistory.length} report
                {diagnosisHistory.length !== 1 ? "s" : ""} in history
              </p>
            </div>

            <div className="flex items-center space-x-3 mt-4 md:mt-0">
              <button
                onClick={() => navigate(ROUTES.DIAGNOSIS)}
                className="btn btn-primary"
              >
                New Diagnosis
              </button>
              <button
                onClick={() => setShowClearConfirm(true)}
                className="btn btn-outline text-red-600 hover:bg-red-50"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Clear History
              </button>
            </div>
          </div>
        </div>

        {/* Clear Confirmation */}
        {showClearConfirm && (
          <div className="card p-6 mb-6 border-red-200 bg-red-50">
            <h3 className="text-lg font-semibold text-red-900 mb-2">
              Clear All History?
            </h3>
            <p className="text-sm text-red-800 mb-4">
              This will permanently delete all diagnosis reports. This action
              cannot be undone.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={handleClearHistory}
                className="btn bg-red-600 text-white hover:bg-red-700"
              >
                Yes, Clear All
              </button>
              <button
                onClick={() => setShowClearConfirm(false)}
                className="btn btn-outline"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Reports Grid */}
        <div className="grid gap-6">
          {diagnosisHistory.map((report) => (
            <div key={report.id} className="card card-hover p-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="flex-1">
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                      <FileText className="w-6 h-6 text-primary-600" />
                    </div>

                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {report.topPrediction}
                      </h3>

                      <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600 mb-3">
                        <span className="flex items-center">
                          <Calendar className="w-4 h-4 mr-1" />
                          {formatDateTime(report.timestamp)}
                        </span>
                        <span className="flex items-center">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          {formatConfidence(report.confidence)} confidence
                        </span>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        {report.symptoms.slice(0, 5).map((symptom, index) => (
                          <span
                            key={index}
                            className="inline-flex items-center px-2.5 py-1 rounded-md bg-gray-100 text-gray-700 text-xs font-medium"
                          >
                            {symptom}
                          </span>
                        ))}
                        {report.symptoms.length > 5 && (
                          <span className="inline-flex items-center px-2.5 py-1 rounded-md bg-gray-100 text-gray-600 text-xs">
                            +{report.symptoms.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3 mt-4 md:mt-0 md:ml-4">
                  <button
                    onClick={() => {
                      setCurrentDiagnosis(report.diagnosis);
                      navigate(ROUTES.RESULTS);
                    }}
                    className="btn btn-outline flex items-center"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    View Details
                  </button>
                  <button
                    onClick={() => handleGenerateReport(report.id)}
                    className="btn btn-secondary flex items-center"
                    disabled={reportLoading}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Generate Report
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Report Preview */}
        <div className="mt-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Report Preview
            </h2>
            {activeReport && (
              <button
                onClick={handleDownloadReport}
                className="btn btn-outline"
              >
                <Download className="w-4 h-4 mr-2" />
                Download JSON
              </button>
            )}
          </div>

          {reportError && (
            <div className="mb-4">
              <ErrorAlert
                message={reportError}
                onClose={() => setReportError(null)}
              />
            </div>
          )}

          {reportLoading ? (
            <div className="card p-6">
              <LoadingSpinner text="Generating report preview..." />
            </div>
          ) : activeReport ? (
            <ReportViewer report={activeReport} />
          ) : (
            <div className="card p-6">
              <p className="text-sm text-gray-600">
                Select a report to generate a preview.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;
