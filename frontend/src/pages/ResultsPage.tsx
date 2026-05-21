/**
 * Results Page - Most Important Page
 * Professional diagnosis results display with inference visualization
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Download,
  Printer,
  Clock,
  AlertCircle,
  Eye,
} from "lucide-react";
import { useDiagnosisStore } from "@/store/diagnosisStore";
import { ROUTES, MEDICAL_DISCLAIMER } from "@/constants";
import { formatDateTime } from "@/utils/formatters";
import DiagnosisCard from "@/components/diagnosis/DiagnosisCard";
import ExplainabilityPanel from "@/components/diagnosis/ExplainabilityPanel";
import RuleAlertPanel from "@/components/diagnosis/RuleAlertPanel";
import ForwardChainingPanel from "@/components/diagnosis/ForwardChainingPanel";
import BackwardChainingPanel from "@/components/diagnosis/BackwardChainingPanel";
import ConfidenceChart from "@/components/charts/ConfidenceChart";
import PredictionRankingChart from "@/components/charts/PredictionRankingChart";
import SymptomDistributionChart from "@/components/charts/SymptomDistributionChart";
import SeverityIndicator from "@/components/diagnosis/SeverityIndicator";
import EmptyState from "@/components/common/EmptyState";
import ErrorAlert from "@/components/common/ErrorAlert";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import ReportViewer from "@/components/reports/ReportViewer";
import ReportPdfModal from "@/components/reports/ReportPdfModal";
import reportApi from "@/api/reportApi";
import { FileQuestion } from "lucide-react";
import { downloadBlob } from "@/utils/fileDownload";
import { useReportPdf, useToast } from "@/hooks";
import type { ReportData } from "@/types";

const ResultsPage = () => {
  const navigate = useNavigate();
  const { currentDiagnosis, patientInfo } = useDiagnosisStore();
  const [reportError, setReportError] = useState<string | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportAction, setReportAction] = useState<
    "preview" | "download" | null
  >(null);
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const toast = useToast();
  const {
    previewOpen,
    previewUrl,
    previewLoading,
    activeReportId,
    openPreview,
    closePreview,
  } = useReportPdf();

  // Redirect if no diagnosis
  if (!currentDiagnosis) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <EmptyState
            icon={FileQuestion}
            title="No Diagnosis Results"
            description="Please complete a diagnosis first to view results."
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

  const { data, timestamp } = currentDiagnosis;
  const {
    top_predictions = [],
    explainability = {
      matched_symptoms: [],
      unmatched_symptoms: [],
      important_features: [],
    },
    rule_engine_flags = [],
    recommendation = null,
    disclaimer = null,
    patient_analysis = {
      severity: "unknown",
      risk_level: "unknown",
      symptoms_processed: 0,
      symptoms_matched: 0,
    },
  } = data || {};

  const handlePrint = () => {
    window.print();
  };

  const ensureReportData = async () => {
    if (!patientInfo) {
      setReportError("Patient information is required to generate a report.");
      toast.error("Patient information is required to generate a report.");
      return;
    }

    const sessionId = data?.session_id;
    if (!sessionId) {
      setReportError("Session ID is required to generate a report.");
      toast.error("Session ID is required to generate a report.");
      return;
    }

    if (reportData) {
      return reportData;
    }

    const response = await reportApi.generate({
      diagnosis_result: data,
      patient_info: patientInfo,
      format: "json",
      session_id: sessionId,
    });

    if (!response?.data) {
      throw new Error("Report generation failed");
    }

    setReportData(response.data);
    return response.data;
  };

  const handleViewReport = async () => {
    try {
      setReportError(null);
      setReportLoading(true);
      setReportAction("preview");

      const report = await ensureReportData();
      if (!report?.report_id) {
        return;
      }

      await openPreview(report.report_id);
      toast.success("Report preview is ready.", "Preview opened");
    } catch (error) {
      toast.error("Failed to open report preview.");
      setReportError("Failed to open report preview. Please try again.");
    } finally {
      setReportLoading(false);
      setReportAction(null);
    }
  };

  const handleDownload = async () => {
    try {
      setReportError(null);
      setReportLoading(true);
      setReportAction("download");

      const report = await ensureReportData();
      if (!report?.report_id) {
        return;
      }

      const response = await reportApi.downloadPdf(report.report_id);
      const filename = response.filename || `${report.report_id}.pdf`;
      downloadBlob(response.data, filename, "application/pdf");
      toast.success("Report downloaded successfully.", "Download complete");
    } catch (error) {
      toast.error("Failed to download PDF report.");
      setReportError("Failed to generate report. Please try again.");
    } finally {
      setReportLoading(false);
      setReportAction(null);
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

  // Get all symptoms for inference visualization
  const allSymptoms = explainability?.matched_symptoms || [];
  const topPrediction =
    top_predictions && top_predictions.length > 0 ? top_predictions[0] : null;

  return (
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(ROUTES.DIAGNOSIS)}
            className="flex items-center text-neutral-600 hover:text-neutral-900 mb-4 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Diagnosis
          </button>

          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-neutral-900 mb-2">
                Diagnosis Results
              </h1>
              <div className="flex items-center space-x-4 text-sm text-neutral-600">
                <span className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  {formatDateTime(timestamp)}
                </span>
                {patientInfo && (
                  <span>
                    Patient: {patientInfo.age}yo {patientInfo.gender}
                  </span>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-3 mt-4 md:mt-0 print-hidden">
              <button
                onClick={handlePrint}
                className="btn btn-outline flex items-center"
              >
                <Printer className="w-4 h-4 mr-2" />
                Print
              </button>
              <button
                onClick={handleViewReport}
                className="btn btn-outline flex items-center"
                disabled={reportLoading}
              >
                <Eye className="w-4 h-4 mr-2" />
                {reportAction === "preview" ? "Generating..." : "View Report"}
              </button>
              <button
                onClick={handleDownload}
                className="btn btn-secondary flex items-center"
                disabled={reportLoading}
              >
                <Download className="w-4 h-4 mr-2" />
                {reportAction === "download" ? "Preparing..." : "Download PDF"}
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

        {/* Medical Disclaimer Banner */}
        <div className="mb-8">
          <div className="bg-blue-50 border border-blue-200 rounded-medical p-4">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-blue-900 mb-1">
                  Important Medical Disclaimer
                </h3>
                <p className="text-sm text-blue-800 leading-relaxed">
                  {disclaimer || MEDICAL_DISCLAIMER}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Rule Engine Alerts */}
        {rule_engine_flags && rule_engine_flags.length > 0 && (
          <div className="mb-8">
            <RuleAlertPanel alerts={rule_engine_flags} />
          </div>
        )}

        {/* Top-3 Predictions */}
        <div className="mb-8">
          <h2 className="section-header">Top 3 Differential Diagnoses</h2>
          {top_predictions && top_predictions.length > 0 ? (
            <div className="grid gap-6">
              {top_predictions.slice(0, 3).map((prediction, index) => (
                <DiagnosisCard
                  key={index}
                  prediction={prediction}
                  rank={index + 1}
                  isTopPrediction={index === 0}
                />
              ))}
            </div>
          ) : (
            <div className="card p-6">
              <p className="text-sm text-neutral-600">
                No predictions available.
              </p>
            </div>
          )}
        </div>

        {/* ACADEMIC REQUIREMENT: Inference Visualization */}
        <div className="mb-8">
          <h2 className="section-header">Clinical Reasoning & Inference</h2>
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Forward Chaining */}
            <ForwardChainingPanel
              symptoms={allSymptoms}
              ruleFlags={rule_engine_flags.map((flag) => ({
                rule: flag.rule_id,
                type: flag.category,
                message: flag.explanation,
              }))}
              predictions={top_predictions.map((pred) => ({
                disease: pred.disease,
                confidence: pred.confidence,
              }))}
            />

            {/* Backward Chaining */}
            {topPrediction ? (
              <BackwardChainingPanel
                topPrediction={{
                  disease: topPrediction.disease,
                  confidence: topPrediction.confidence,
                  matched_symptoms: explainability.matched_symptoms,
                }}
                allSymptoms={allSymptoms}
                explainability={explainability}
              />
            ) : (
              <div className="card p-6">
                <p className="text-sm text-neutral-600">
                  No top prediction available for backward chaining.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Charts and Visualizations */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <ConfidenceChart predictions={top_predictions || []} />
          <PredictionRankingChart predictions={top_predictions || []} />
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <SeverityIndicator
            severity={patient_analysis.severity}
            riskLevel={patient_analysis.risk_level}
            symptomsProcessed={patient_analysis.symptoms_processed}
            symptomsMatched={patient_analysis.symptoms_matched}
          />
          <SymptomDistributionChart
            matchedCount={explainability.matched_symptoms?.length || 0}
            unmatchedCount={explainability.unmatched_symptoms?.length || 0}
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <ExplainabilityPanel explainability={explainability} />
          <div>
            <h3 className="subsection-header">Report Preview</h3>
            {reportLoading && reportAction === "preview" ? (
              <LoadingSpinner text="Generating report preview..." />
            ) : reportData ? (
              <ReportViewer report={reportData} />
            ) : (
              <div className="card p-6">
                <p className="text-sm text-neutral-600">
                  Generate a report to preview the clinical summary.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Recommendations */}
        {recommendation && (
          <div className="card p-6 mb-8">
            <h3 className="subsection-header">Clinical Recommendations</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-xs font-semibold text-primary-700">
                    1
                  </span>
                </div>
                <p className="text-sm text-neutral-700">{recommendation}</p>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center print-hidden">
          <button
            onClick={() => navigate(ROUTES.DIAGNOSIS)}
            className="btn btn-primary px-8 py-3"
          >
            Start New Diagnosis
          </button>
          <button
            onClick={() => navigate(ROUTES.REPORTS)}
            className="btn btn-outline px-8 py-3"
          >
            View All Reports
          </button>
        </div>

        {/* Footer Note */}
        <div className="mt-8 text-center">
          <p className="text-sm text-neutral-500">
            This diagnosis was generated using AI-powered analysis combined with
            clinical validation rules.
            <br />
            Always consult with a qualified healthcare professional for medical
            advice.
          </p>
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

export default ResultsPage;
