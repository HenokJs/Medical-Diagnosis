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
import { useDiagnosisStore } from "@/store/diagnosisStore";
import { formatDateTime, formatConfidence } from "@/utils/formatters";
import EmptyState from "@/components/common/EmptyState";
import { ROUTES } from "@/constants";
import reportApi from "@/api/reportApi";
import ErrorAlert from "@/components/common/ErrorAlert";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import type { DiagnosisResponse } from "@/types";

const ReportsPage = () => {
  const navigate = useNavigate();
  const { setCurrentDiagnosis } = useDiagnosisStore();
  
  // State for database reports
  const [dbReports, setDbReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
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
      console.error("Failed to fetch reports:", err);
      setError("Failed to load report history. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (session: any) => {
    // Reconstruct diagnosis object for viewing - must match DiagnosisResponse structure
    const diagnosis: DiagnosisResponse = {
      success: true,
      message: "Diagnosis retrieved from history",
      data: {
        success: true,
        top_predictions: session.predictions || [],
        explainability: {
          matched_symptoms: session.extracted_symptoms?.filter((s: any) => s.matched_in_model).map((s: any) => s.symptom_name) || [],
          unmatched_symptoms: session.extracted_symptoms?.filter((s: any) => !s.matched_in_model).map((s: any) => s.symptom_name) || [],
          important_features: [],
        },
        rule_engine_flags: session.rule_alerts || [],
        patient_analysis: {
          severity: session.overall_severity || "unknown",
          risk_level: session.risk_level || "unknown",
          symptoms_processed: session.symptoms_processed || 0,
          symptoms_matched: session.symptoms_matched || 0,
        },
      },
      timestamp: session.created_at,
    };
    
    setCurrentDiagnosis(diagnosis);
    navigate(ROUTES.RESULTS);
  };

  const handleDownloadPDF = async (session: any) => {
    try {
      setReportError(null);
      setReportLoading(true);
      
      // Prepare data for PDF generation - must match DiagnosisData structure
      const diagnosisData = {
        success: true,
        top_predictions: session.predictions || [],
        explainability: {
          matched_symptoms: session.extracted_symptoms?.filter((s: any) => s.matched_in_model).map((s: any) => s.symptom_name) || [],
          unmatched_symptoms: session.extracted_symptoms?.filter((s: any) => !s.matched_in_model).map((s: any) => s.symptom_name) || [],
          important_features: [],
        },
        rule_engine_flags: session.rule_alerts || [],
        patient_analysis: {
          severity: session.overall_severity || "unknown",
          risk_level: session.risk_level || "unknown",
          symptoms_processed: session.symptoms_processed || 0,
          symptoms_matched: session.symptoms_matched || 0,
        },
      };
      
      const patientInfo = {
        age: session.patient?.age || 0,
        gender: session.patient?.gender || "unknown",
        patient_id: session.patient?.patient_id,
      };
      
      const response = await reportApi.generate({
        diagnosis_result: diagnosisData,
        patient_info: patientInfo,
        format: "pdf",
      });

      // If response is a blob (PDF), download it
      if (response.data instanceof Blob) {
        const url = URL.createObjectURL(response.data);
        const link = document.createElement("a");
        link.href = url;
        link.download = `diagnosis_report_${session.session_id}.pdf`;
        link.click();
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error("PDF generation error:", error);
      setReportError("Failed to generate PDF. Please try again.");
    } finally {
      setReportLoading(false);
    }
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
                {dbReports.length} report{dbReports.length !== 1 ? "s" : ""} in history
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
            const topPrediction = session.predictions && session.predictions.length > 0 
              ? session.predictions[0] 
              : null;
            const symptoms = session.extracted_symptoms?.map((s: any) => s.symptom_name) || [];
            
            return (
              <div key={session.id} className="card card-hover p-6">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                        <FileText className="w-6 h-6 text-primary-600" />
                      </div>

                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {topPrediction?.disease_name || "Diagnosis Session"}
                        </h3>

                        <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600 mb-3">
                          <span className="flex items-center">
                            <Calendar className="w-4 h-4 mr-1" />
                            {formatDateTime(session.created_at)}
                          </span>
                          {topPrediction && (
                            <span className="flex items-center">
                              <TrendingUp className="w-4 h-4 mr-1" />
                              {formatConfidence(topPrediction.confidence_score)} confidence
                            </span>
                          )}
                          <span className="inline-flex items-center px-2 py-1 rounded-md bg-blue-100 text-blue-700 text-xs font-medium">
                            {session.session_id}
                          </span>
                        </div>

                        <div className="flex flex-wrap gap-2">
                          {symptoms.slice(0, 5).map((symptom: string, index: number) => (
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
                      onClick={() => handleViewDetails(session)}
                      className="btn btn-outline flex items-center"
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      View Details
                    </button>
                    <button
                      onClick={() => handleDownloadPDF(session)}
                      className="btn btn-secondary flex items-center"
                      disabled={reportLoading}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download PDF
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;
