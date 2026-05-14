/**
 * Report Viewer
 * Structured report preview and print view
 */

import type { ReportData } from "@/types";
import SeverityBadge from "@/components/common/SeverityBadge";
import {
  formatDateTime,
  formatSeverityLabel,
  formatRiskLevel,
} from "@/utils/formatters";

interface ReportViewerProps {
  report: ReportData;
}

const ReportViewer = ({ report }: ReportViewerProps) => {
  // Null safety checks
  if (!report) {
    return (
      <div className="card p-6">
        <p className="text-sm text-neutral-600">No report data available</p>
      </div>
    );
  }

  const patientInfo = report?.patient_info || {};
  const diagnosis = report?.diagnosis || {};
  const topPredictions = diagnosis?.top_predictions || [];
  const clinicalFindings = report?.clinical_findings || {};
  const symptoms = clinicalFindings?.symptoms || [];
  const ruleFlags = clinicalFindings?.rule_flags || [];

  return (
    <div className="card p-6 print:shadow-none print:border-none">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Clinical Report</h2>
          <p className="text-sm text-gray-600">Report ID: {report?.report_id || "N/A"}</p>
        </div>
        <div className="text-sm text-gray-600">
          Generated: {report?.generated_at ? formatDateTime(report.generated_at) : "N/A"}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Patient Information
          </h3>
          <div className="text-sm text-gray-700 space-y-1">
            {patientInfo?.name && (
              <p>Name: {patientInfo.name}</p>
            )}
            {patientInfo?.patient_id && (
              <p>ID: {patientInfo.patient_id}</p>
            )}
            <p>Age: {patientInfo?.age || "N/A"}</p>
            <p>Gender: {patientInfo?.gender || "N/A"}</p>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Diagnosis Summary
          </h3>
          <div className="text-sm text-gray-700 space-y-2">
            <div className="flex items-center space-x-2">
              <span>Severity:</span>
              <SeverityBadge
                severity={diagnosis?.severity || "unknown"}
                size="sm"
              />
            </div>
            <p>
              Risk Level:{" "}
              {formatRiskLevel(diagnosis?.risk_level || "unknown")}
            </p>
          </div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Top Predictions
        </h3>
        {topPredictions && topPredictions.length > 0 ? (
          <div className="space-y-3">
            {topPredictions
              .slice(0, 3)
              .map((prediction, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between text-sm"
                >
                  <div>
                    <p className="font-medium text-gray-900">
                      {prediction?.disease || prediction?.disease_name || "Unknown"}
                    </p>
                    <p className="text-gray-600">
                      Severity:{" "}
                      {formatSeverityLabel(prediction?.severity || "unknown")}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-gray-900">
                      {((prediction?.confidence || prediction?.confidence_score || 0) * 100).toFixed(1)}%
                    </p>
                    <p className="text-xs text-gray-500">Confidence</p>
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <p className="text-sm text-gray-600">No predictions available</p>
        )}
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Clinical Findings
        </h3>
        <div className="text-sm text-gray-700 space-y-2">
          <p>
            Matched Symptoms:{" "}
            {symptoms && symptoms.length > 0 ? symptoms.join(", ") : "None"}
          </p>
          <p>Rule Alerts: {ruleFlags?.length || 0}</p>
        </div>
      </div>

      {report?.recommendation && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Recommendation
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            {report.recommendation}
          </p>
        </div>
      )}

      {report?.disclaimer && (
        <div className="border-t border-gray-200 pt-4">
          <p className="text-xs text-gray-600 leading-relaxed">
            {report.disclaimer}
          </p>
        </div>
      )}
    </div>
  );
};

export default ReportViewer;
