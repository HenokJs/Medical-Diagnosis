/**
 * Forward Chaining Panel
 * Displays: Symptoms → Triggered Rules → Possible Diseases
 * Academic Requirement: Visible Forward Chaining Inference
 */

import { ArrowRight, Activity, AlertTriangle } from 'lucide-react';

interface ForwardChain {
  symptoms: string[];
  triggered_rules: Array<{
    rule: string;
    message: string;
    diseases: string[];
  }>;
  possible_diseases: string[];
}

interface ForwardChainingPanelProps {
  chains?: ForwardChain;
  symptoms: string[];
  ruleFlags?: Array<{
    rule: string;
    type: string;
    message: string;
  }>;
  predictions?: Array<{
    disease: string;
    confidence: number;
  }>;
}

const ForwardChainingPanel = ({ 
  chains, 
  symptoms = [], 
  ruleFlags = [], 
  predictions = [] 
}: ForwardChainingPanelProps) => {
  // Null safety checks
  if (!symptoms || symptoms.length === 0) {
    return (
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
          <Activity className="w-5 h-5 mr-2 text-primary-blue" />
          Forward Chaining Inference
        </h3>
        <div className="flex items-center justify-center h-64 text-neutral-500">
          <p className="text-sm">No symptom data available for forward chaining</p>
        </div>
      </div>
    );
  }

  // Build forward chain from available data
  const triggeredRules = (ruleFlags || []).map(flag => ({
    rule: flag?.rule || flag?.name || "Unknown Rule",
    message: flag?.message || flag?.explanation || "",
    type: flag?.type || flag?.alert_type || "info",
    diseases: (predictions || []).slice(0, 3).map(p => p?.disease || p?.disease_name || "Unknown")
  }));

  const possibleDiseases = (predictions || []).slice(0, 3).map(p => p?.disease || p?.disease_name || "Unknown");

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
        <Activity className="w-5 h-5 mr-2 text-primary-blue" />
        Forward Chaining Inference
      </h3>
      
      <p className="text-sm text-neutral-600 mb-4">
        Reasoning: Symptoms → Rules → Possible Diseases
      </p>

      <div className="space-y-4">
        {/* Step 1: Input Symptoms */}
        <div className="bg-medical-light border border-medical-cyan rounded-medical p-4">
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              1
            </div>
            <h4 className="font-semibold text-neutral-900">Input Symptoms</h4>
          </div>
          <div className="ml-11 flex flex-wrap gap-2">
            {symptoms.map((symptom, idx) => (
              <span
                key={idx}
                className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-white border border-medical-cyan text-primary-dark"
              >
                {symptom}
              </span>
            ))}
          </div>
        </div>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowRight className="w-6 h-6 text-primary-blue" />
        </div>

        {/* Step 2: Triggered Rules */}
        <div className="bg-blue-50 border border-blue-200 rounded-medical p-4">
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              2
            </div>
            <h4 className="font-semibold text-neutral-900">Triggered Rules</h4>
          </div>
          <div className="ml-11 space-y-2">
            {triggeredRules.length > 0 ? (
              triggeredRules.map((rule, idx) => (
                <div
                  key={idx}
                  className="bg-white border border-blue-300 rounded p-3"
                >
                  <div className="flex items-start">
                    <AlertTriangle className={`w-4 h-4 mr-2 mt-0.5 ${
                      rule.type === 'urgent' ? 'text-red-600' : 
                      rule.type === 'warning' ? 'text-amber-600' : 
                      'text-blue-600'
                    }`} />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-neutral-900">
                        {rule.rule}
                      </p>
                      <p className="text-xs text-neutral-600 mt-1">
                        {rule.message}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="bg-white border border-blue-200 rounded p-3">
                <p className="text-sm text-neutral-600">
                  No specific clinical rules triggered. Proceeding with ML-based analysis.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowRight className="w-6 h-6 text-primary-blue" />
        </div>

        {/* Step 3: Possible Diseases */}
        <div className="bg-green-50 border border-green-200 rounded-medical p-4">
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              3
            </div>
            <h4 className="font-semibold text-neutral-900">Possible Diseases</h4>
          </div>
          <div className="ml-11 space-y-2">
            {possibleDiseases.map((disease, idx) => {
              const prediction = predictions[idx] || {};
              const confidence = prediction?.confidence || prediction?.confidence_score || 0;
              return (
                <div
                  key={idx}
                  className="bg-white border border-green-300 rounded p-3 flex items-center justify-between"
                >
                  <div className="flex items-center">
                    <span className="w-6 h-6 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-xs font-semibold mr-3">
                      {idx + 1}
                    </span>
                    <span className="text-sm font-medium text-neutral-900">
                      {disease}
                    </span>
                  </div>
                  <span className="text-xs font-semibold text-green-700">
                    {(confidence * 100).toFixed(1)}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-neutral-50 rounded border border-neutral-200">
        <p className="text-xs text-neutral-600">
          <strong>Forward Chaining Logic:</strong> The system analyzes input symptoms, 
          evaluates clinical rules, and identifies possible diseases based on symptom patterns 
          and medical knowledge.
        </p>
      </div>
    </div>
  );
};

export default ForwardChainingPanel;
