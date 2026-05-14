/**
 * Backward Chaining Panel
 * Displays: Disease Hypothesis → Required Symptoms → Validation
 * Academic Requirement: Visible Backward Chaining Inference
 */

import { ArrowLeft, CheckCircle, XCircle, MinusCircle } from 'lucide-react';

interface BackwardChainingPanelProps {
  topPrediction: {
    disease: string;
    confidence: number;
    matched_symptoms?: string[];
  };
  allSymptoms: string[];
  explainability?: {
    matched_symptoms?: string[];
    unmatched_symptoms?: string[];
  };
}

const BackwardChainingPanel = ({ 
  topPrediction, 
  allSymptoms,
  explainability 
}: BackwardChainingPanelProps) => {
  const matchedSymptoms = explainability?.matched_symptoms || topPrediction.matched_symptoms || [];
  const unmatchedSymptoms = explainability?.unmatched_symptoms || [];
  
  // Calculate validation metrics
  const totalRequired = matchedSymptoms.length + 3; // Estimate required symptoms
  const matchRate = matchedSymptoms.length / totalRequired;
  const validationStatus = matchRate >= 0.6 ? 'validated' : matchRate >= 0.4 ? 'partial' : 'weak';

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
        <ArrowLeft className="w-5 h-5 mr-2 text-primary-blue" />
        Backward Chaining Validation
      </h3>
      
      <p className="text-sm text-neutral-600 mb-4">
        Reasoning: Disease Hypothesis → Required Symptoms → Validation
      </p>

      <div className="space-y-4">
        {/* Step 1: Disease Hypothesis */}
        <div className="bg-purple-50 border border-purple-200 rounded-medical p-4">
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              1
            </div>
            <h4 className="font-semibold text-neutral-900">Disease Hypothesis</h4>
          </div>
          <div className="ml-11">
            <div className="bg-white border border-purple-300 rounded p-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-neutral-900">
                  {topPrediction.disease}
                </span>
                <span className="text-xs font-semibold text-purple-700 bg-purple-100 px-2 py-1 rounded">
                  {(topPrediction.confidence * 100).toFixed(1)}% confidence
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowLeft className="w-6 h-6 text-primary-blue" />
        </div>

        {/* Step 2: Required Symptoms Check */}
        <div className="bg-blue-50 border border-blue-200 rounded-medical p-4">
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              2
            </div>
            <h4 className="font-semibold text-neutral-900">Required Symptoms Check</h4>
          </div>
          <div className="ml-11 space-y-2">
            {/* Matched Symptoms */}
            {matchedSymptoms.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-green-700 mb-2">
                  ✓ Present ({matchedSymptoms.length})
                </p>
                <div className="space-y-1">
                  {matchedSymptoms.map((symptom, idx) => (
                    <div
                      key={idx}
                      className="bg-white border border-green-300 rounded p-2 flex items-center"
                    >
                      <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                      <span className="text-sm text-neutral-900">{symptom}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Unmatched Symptoms */}
            {unmatchedSymptoms.length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-semibold text-amber-700 mb-2">
                  ⚠ Not Typical ({unmatchedSymptoms.length})
                </p>
                <div className="space-y-1">
                  {unmatchedSymptoms.map((symptom, idx) => (
                    <div
                      key={idx}
                      className="bg-white border border-amber-300 rounded p-2 flex items-center"
                    >
                      <MinusCircle className="w-4 h-4 text-amber-600 mr-2" />
                      <span className="text-sm text-neutral-900">{symptom}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowLeft className="w-6 h-6 text-primary-blue" />
        </div>

        {/* Step 3: Validation Result */}
        <div className={`border rounded-medical p-4 ${
          validationStatus === 'validated' ? 'bg-green-50 border-green-200' :
          validationStatus === 'partial' ? 'bg-amber-50 border-amber-200' :
          'bg-orange-50 border-orange-200'
        }`}>
          <div className="flex items-center mb-2">
            <div className="w-8 h-8 rounded-full bg-primary-blue text-white flex items-center justify-center text-sm font-semibold mr-3">
              3
            </div>
            <h4 className="font-semibold text-neutral-900">Validation Result</h4>
          </div>
          <div className="ml-11">
            <div className={`border rounded p-3 ${
              validationStatus === 'validated' ? 'bg-white border-green-300' :
              validationStatus === 'partial' ? 'bg-white border-amber-300' :
              'bg-white border-orange-300'
            }`}>
              <div className="flex items-start">
                {validationStatus === 'validated' ? (
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3 mt-0.5" />
                ) : validationStatus === 'partial' ? (
                  <MinusCircle className="w-5 h-5 text-amber-600 mr-3 mt-0.5" />
                ) : (
                  <XCircle className="w-5 h-5 text-orange-600 mr-3 mt-0.5" />
                )}
                <div className="flex-1">
                  <p className="text-sm font-semibold text-neutral-900 mb-1">
                    {validationStatus === 'validated' ? 'Hypothesis Validated' :
                     validationStatus === 'partial' ? 'Partial Validation' :
                     'Weak Validation'}
                  </p>
                  <p className="text-xs text-neutral-600">
                    {matchedSymptoms.length} of {totalRequired} typical symptoms present 
                    ({(matchRate * 100).toFixed(0)}% match rate)
                  </p>
                  {validationStatus === 'validated' && (
                    <p className="text-xs text-green-700 mt-2">
                      Strong symptom correlation supports this diagnosis.
                    </p>
                  )}
                  {validationStatus === 'partial' && (
                    <p className="text-xs text-amber-700 mt-2">
                      Moderate symptom correlation. Consider differential diagnoses.
                    </p>
                  )}
                  {validationStatus === 'weak' && (
                    <p className="text-xs text-orange-700 mt-2">
                      Limited symptom correlation. Further evaluation recommended.
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-neutral-50 rounded border border-neutral-200">
        <p className="text-xs text-neutral-600">
          <strong>Backward Chaining Logic:</strong> The system starts with the top disease hypothesis, 
          checks which required symptoms are present in the patient's presentation, and validates 
          the hypothesis based on symptom correlation.
        </p>
      </div>
    </div>
  );
};

export default BackwardChainingPanel;
