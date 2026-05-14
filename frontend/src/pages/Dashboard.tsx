/**
 * Professional Dashboard / Landing Page
 * Clean, medical-grade overview
 */

import { Link } from "react-router-dom";
import {
  Activity,
  Brain,
  FileText,
  TrendingUp,
  ArrowRight,
  Shield,
  Zap,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import diagnosisApi from "@/api/diagnosisApi";
import { ROUTES } from "@/constants";
import LoadingSpinner from "@/components/common/LoadingSpinner";

const Dashboard = () => {
  // Fetch system health
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ["health"],
    queryFn: diagnosisApi.getHealth,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Fetch model info
  const { data: modelInfo, isLoading: modelLoading } = useQuery({
    queryKey: ["modelInfo"],
    queryFn: diagnosisApi.getModelInfo,
  });

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Diagnosis",
      description:
        "Advanced machine learning models trained on 55,000+ medical cases",
      color: "text-blue-600",
      bg: "bg-blue-50",
    },
    {
      icon: TrendingUp,
      title: "99.68% Top-3 Accuracy",
      description:
        "Industry-leading accuracy in differential diagnosis predictions",
      color: "text-green-600",
      bg: "bg-green-50",
    },
    {
      icon: Shield,
      title: "Clinical Safety",
      description:
        "Rule-based validation and explainable AI for transparent decisions",
      color: "text-purple-600",
      bg: "bg-purple-50",
    },
    {
      icon: Zap,
      title: "Real-Time Analysis",
      description: "Sub-second inference with comprehensive explainability",
      color: "text-amber-600",
      bg: "bg-amber-50",
    },
  ];

  const quickActions = [
    {
      title: "New Diagnosis",
      description: "Start a new patient diagnosis",
      icon: Activity,
      href: ROUTES.DIAGNOSIS,
      color: "bg-primary-600 hover:bg-primary-700",
    },
    {
      title: "View Reports",
      description: "Access diagnosis history",
      icon: FileText,
      href: ROUTES.REPORTS,
      color: "bg-gray-600 hover:bg-gray-700",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-16">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 mb-6">
            <Activity className="w-8 h-8 text-primary-600" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Medical Diagnosis Decision Support
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            AI-powered clinical decision support system combining machine
            learning, rule-based reasoning, and explainable AI for accurate
            diagnosis
          </p>
        </div>

        {/* System Status Banner */}
        {!healthLoading && health && (
          <div className="mb-12">
            <div
              className={`card p-4 ${health.status === "healthy" ? "border-green-200 bg-green-50" : "border-amber-200 bg-amber-50"}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div
                    className={`w-3 h-3 rounded-full ${health.status === "healthy" ? "bg-green-500" : "bg-amber-500"} animate-pulse`}
                  />
                  <span className="font-medium text-gray-900">
                    System Status:{" "}
                    {health.status === "healthy" ? "Operational" : "Degraded"}
                  </span>
                  <span className="text-sm text-gray-600">
                    • Uptime: {health.uptime}
                  </span>
                </div>
                <Link
                  to={ROUTES.STATUS}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  View Details →
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          {quickActions.map((action) => (
            <Link
              key={action.title}
              to={action.href}
              className={`card card-hover p-8 ${action.color} text-white group`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-2xl font-semibold mb-2">
                    {action.title}
                  </h3>
                  <p className="text-white/90">{action.description}</p>
                </div>
                <action.icon className="w-12 h-12 opacity-80 group-hover:opacity-100 transition-opacity" />
              </div>
              <div className="mt-6 flex items-center text-white/90 group-hover:text-white">
                <span className="text-sm font-medium">Get Started</span>
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
          ))}
        </div>

        {/* Features Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            System Capabilities
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => (
              <div key={feature.title} className="card card-hover p-6">
                <div
                  className={`w-12 h-12 rounded-lg ${feature.bg} flex items-center justify-center mb-4`}
                >
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Metrics */}
        {!modelLoading && modelInfo && (
          <div className="card p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              Model Performance
            </h2>
            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600 mb-2">
                  {typeof modelInfo.accuracy === "number"
                    ? `${(modelInfo.accuracy * 100).toFixed(1)}%`
                    : "N/A"}
                </div>
                <div className="text-sm text-gray-600">Model Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {typeof modelInfo.top3_accuracy === "number"
                    ? `${(modelInfo.top3_accuracy * 100).toFixed(1)}%`
                    : "N/A"}
                </div>
                <div className="text-sm text-gray-600">Top-3 Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {modelInfo.num_diseases}
                </div>
                <div className="text-sm text-gray-600">Diseases</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-amber-600 mb-2">
                  {modelInfo.num_features}
                </div>
                <div className="text-sm text-gray-600">Symptoms</div>
              </div>
            </div>
          </div>
        )}

        {modelLoading && (
          <div className="card p-8">
            <LoadingSpinner text="Loading model information..." />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
