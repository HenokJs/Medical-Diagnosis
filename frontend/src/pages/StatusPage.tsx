/**
 * System Status Page
 * Real-time system health monitoring
 */

import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  CheckCircle,
  XCircle,
  Clock,
  Database,
  Cpu,
  TrendingUp,
} from "lucide-react";
import diagnosisApi from "@/api/diagnosisApi";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import { formatDateTime } from "@/utils/formatters";

const StatusPage = () => {
  // Fetch health status
  const {
    data: health,
    isLoading: healthLoading,
    error: healthError,
  } = useQuery({
    queryKey: ["health"],
    queryFn: diagnosisApi.getHealth,
    refetchInterval: 10000, // Refetch every 10 seconds
  });

  // Fetch model info
  const { data: modelInfo, isLoading: modelLoading } = useQuery({
    queryKey: ["modelInfo"],
    queryFn: diagnosisApi.getModelInfo,
  });

  // Fetch stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["stats"],
    queryFn: diagnosisApi.getStats,
  });

  const { data: latencyMs } = useQuery({
    queryKey: ["ping"],
    queryFn: async () => {
      const start = performance.now();
      await diagnosisApi.ping();
      return Math.round(performance.now() - start);
    },
    refetchInterval: 15000,
  });

  const isHealthy = health?.status === "healthy";

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            System Status
          </h1>
          <p className="text-gray-600">
            Real-time monitoring of system health and performance
          </p>
        </div>

        {/* Overall Status Banner */}
        <div className="mb-8">
          {healthLoading ? (
            <div className="card p-6">
              <LoadingSpinner text="Checking system status..." />
            </div>
          ) : healthError ? (
            <div className="card p-6 border-red-200 bg-red-50">
              <div className="flex items-center space-x-3">
                <XCircle className="w-8 h-8 text-red-600" />
                <div>
                  <h3 className="text-lg font-semibold text-red-900">
                    System Offline
                  </h3>
                  <p className="text-sm text-red-700">
                    Unable to connect to backend services. Please check your
                    connection.
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div
              className={`card p-6 ${
                isHealthy
                  ? "border-green-200 bg-green-50"
                  : "border-amber-200 bg-amber-50"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  {isHealthy ? (
                    <CheckCircle className="w-10 h-10 text-green-600" />
                  ) : (
                    <Activity className="w-10 h-10 text-amber-600 animate-pulse" />
                  )}
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      {isHealthy
                        ? "All Systems Operational"
                        : "System Degraded"}
                    </h3>
                    <p className="text-sm text-gray-700">
                      Last checked:{" "}
                      {formatDateTime(
                        health?.timestamp || new Date().toISOString(),
                      )}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      isHealthy ? "bg-green-500" : "bg-amber-500"
                    } animate-pulse`}
                  />
                  <span className="text-sm font-medium text-gray-700">
                    {isHealthy ? "Healthy" : "Degraded"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* System Metrics Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Uptime */}
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <Clock className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Uptime</h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {health?.uptime || "N/A"}
            </p>
          </div>

          {/* ML Models Status */}
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                <Database className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">ML Models</h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {health?.models_loaded ? (
                <span className="text-green-600">Loaded</span>
              ) : (
                <span className="text-red-600">Not Loaded</span>
              )}
            </p>
          </div>

          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">
                API Latency
              </h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {latencyMs ? `${latencyMs}ms` : "N/A"}
            </p>
          </div>

          {/* Model Accuracy */}
          {!modelLoading && modelInfo && (
            <>
              <div className="card p-6">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-green-600" />
                  </div>
                  <h3 className="text-sm font-semibold text-gray-700">
                    Accuracy
                  </h3>
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  {typeof modelInfo.accuracy === "number"
                    ? `${(modelInfo.accuracy * 100).toFixed(1)}%`
                    : "N/A"}
                </p>
              </div>

              <div className="card p-6">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
                    <Cpu className="w-6 h-6 text-amber-600" />
                  </div>
                  <h3 className="text-sm font-semibold text-gray-700">
                    Top-3 Accuracy
                  </h3>
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  {typeof modelInfo.top3_accuracy === "number"
                    ? `${(modelInfo.top3_accuracy * 100).toFixed(2)}%`
                    : "N/A"}
                </p>
              </div>
            </>
          )}
        </div>

        {/* Model Information */}
        {!modelLoading && modelInfo && (
          <div className="card p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Model Information
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Model Type</p>
                <p className="text-lg font-semibold text-gray-900">
                  {modelInfo.model_type}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Diseases</p>
                <p className="text-lg font-semibold text-gray-900">
                  {modelInfo.num_diseases}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Features</p>
                <p className="text-lg font-semibold text-gray-900">
                  {modelInfo.num_features}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Training Date</p>
                <p className="text-sm font-medium text-gray-900">
                  {modelInfo.training_date
                    ? formatDateTime(modelInfo.training_date)
                    : "N/A"}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* System Statistics */}
        {!statsLoading && stats && (
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              System Statistics
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Model Type</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.model?.type || "N/A"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Diseases</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.data?.diseases ?? "N/A"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Symptoms</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.data?.symptoms ?? "N/A"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Clinical Rules</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.data?.rules ?? "N/A"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">API Version</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.system?.version || "N/A"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Environment</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.system?.environment || "N/A"}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Loading States */}
        {(modelLoading || statsLoading) && (
          <div className="card p-6">
            <LoadingSpinner text="Loading system information..." />
          </div>
        )}
      </div>
    </div>
  );
};

export default StatusPage;
