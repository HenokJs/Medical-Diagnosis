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
  return (
    <div className="card p-6 print:shadow-none print:border-none">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Clinical Report</h2>
          <p className="text-sm text-gray-600">Report ID: {report.report_id}</p>
        </div>
        <div className="text-sm text-gray-600">
          Generated: {formatDateTime(report.generated_at)}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Patient Information
          </h3>
          <div className="text-sm text-gray-700 space-y-1">
            {report.patient_info.name && (
              <p>Name: {report.patient_info.name}</p>
            )}
            {report.patient_info.patient_id && (
              <p>ID: {report.patient_info.patient_id}</p>
            )}
            <p>Age: {report.patient_info.age}</p>
            <p>Gender: {report.patient_info.gender}</p>
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
                severity={report.diagnosis.severity || "unknown"}
                size="sm"
              />
            </div>
            <p>
              Risk Level:{" "}
              {formatRiskLevel(report.diagnosis.risk_level || "unknown")}
            </p>
          </div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Top Predictions
        </h3>
        <div className="space-y-3">
          {report.diagnosis.top_predictions
            .slice(0, 3)
            .map((prediction, index) => (
              <div
                key={index}
                className="flex items-center justify-between text-sm"
              >
                <div>
                  <p className="font-medium text-gray-900">
                    {prediction.disease}
                  </p>
                  <p className="text-gray-600">
                    Severity:{" "}
                    {formatSeverityLabel(prediction.severity || "unknown")}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    {(prediction.confidence * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-500">Confidence</p>
                </div>
              </div>
            ))}
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Clinical Findings
        </h3>
        <div className="text-sm text-gray-700 space-y-2">
          <p>
            Matched Symptoms:{" "}
            {report.clinical_findings.symptoms.join(", ") || "None"}
          </p>
          <p>Rule Alerts: {report.clinical_findings.rule_flags.length}</p>
        </div>
      </div>

      {report.recommendation && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Recommendation
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            {report.recommendation}
          </p>
        </div>
      )}

      {report.disclaimer && (
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
