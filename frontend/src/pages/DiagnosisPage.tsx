import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { User, Calendar, Activity } from "lucide-react";
import WorkingSymptomInput from "@/components/diagnosis/WorkingSymptomInput";
import diagnosisApi from "@/api/diagnosisApi";
import { useDiagnosisStore } from "@/store/diagnosisStore";
import { ROUTES } from "@/constants";
import { parseDurationDays } from "@/utils/formatters";
import ErrorAlert from "@/components/common/ErrorAlert";
import type { PatientInfo } from "@/types";

const DiagnosisPage = () => {
  const navigate = useNavigate();
  const {
    selectedSymptoms,
    setSelectedSymptoms,
    setPatientInfo,
    setCurrentDiagnosis,
    addToHistory,
  } = useDiagnosisStore();

  const [patientData, setPatientData] = useState<PatientInfo>({
    age: 30,
    gender: "male",
    symptomDuration: "",
    notes: "",
  });

  const [freeText, setFreeText] = useState("");

  // Diagnosis mutation
  const diagnosisMutation = useMutation({
    mutationFn: diagnosisApi.predict,
    onSuccess: (data) => {
      setCurrentDiagnosis(data);
      addToHistory(data);
      setPatientInfo(patientData);
      navigate(ROUTES.RESULTS);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedSymptoms.length === 0 && !freeText) {
      alert("Please enter at least one symptom");
      return;
    }

    const durationDays = parseDurationDays(patientData.symptomDuration || "");

    diagnosisMutation.mutate({
      symptoms: selectedSymptoms,
      age: patientData.age,
      gender: patientData.gender,
      duration_days: durationDays,
      free_text: freeText || undefined,
    });
  };

  const canSubmit = selectedSymptoms.length > 0 || freeText.trim().length > 0;

  return (
    <div className="min-h-screen bg-primary-50 py-6">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary-600 flex items-center justify-center shadow-sm">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-dark">
                New Diagnosis
              </h1>
              <p className="text-sm text-primary-700">
                Enter symptoms and patient information
              </p>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {diagnosisMutation.isError && (
          <div className="mb-4">
            <ErrorAlert
              message="Failed to process diagnosis. Please check your connection and try again."
              onClose={() => diagnosisMutation.reset()}
            />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Working Symptom Input */}
          <WorkingSymptomInput
            selectedSymptoms={selectedSymptoms}
            onSymptomsChange={setSelectedSymptoms}
            freeText={freeText}
            onFreeTextChange={setFreeText}
          />

          {/* Patient Information */}
          <div className="card p-5">
            <div className="flex items-center gap-2 mb-4">
              <User className="w-5 h-5 text-primary-600" />
              <h3 className="text-base font-semibold text-primary-dark">
                Patient Information
              </h3>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-primary-800 mb-1.5">
                  Age *
                </label>
                <input
                  type="number"
                  value={patientData.age}
                  onChange={(e) =>
                    setPatientData({
                      ...patientData,
                      age: parseInt(e.target.value) || 0,
                    })
                  }
                  min="0"
                  max="120"
                  required
                  className="input text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-primary-800 mb-1.5">
                  Gender *
                </label>
                <select
                  value={patientData.gender}
                  onChange={(e) =>
                    setPatientData({
                      ...patientData,
                      gender: e.target.value as "male" | "female" | "other",
                    })
                  }
                  required
                  className="input text-sm"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-primary-800 mb-1.5 flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  Symptom Duration
                </label>
                <input
                  type="text"
                  value={patientData.symptomDuration}
                  onChange={(e) =>
                    setPatientData({
                      ...patientData,
                      symptomDuration: e.target.value,
                    })
                  }
                  placeholder="e.g., 3 days"
                  className="input text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-primary-800 mb-1.5">
                  Notes
                </label>
                <input
                  type="text"
                  value={patientData.notes}
                  onChange={(e) =>
                    setPatientData({ ...patientData, notes: e.target.value })
                  }
                  placeholder="Additional information"
                  className="input text-sm"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-2">
            <p className="text-sm text-primary-700">
              {selectedSymptoms.length} symptom
              {selectedSymptoms.length !== 1 ? "s" : ""} selected
            </p>
            <button
              type="submit"
              disabled={!canSubmit || diagnosisMutation.isPending}
              className="btn btn-primary px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {diagnosisMutation.isPending
                ? "Analyzing..."
                : "Analyze Symptoms"}
            </button>
          </div>
        </form>

        {/* Loading State */}
        {diagnosisMutation.isPending && (
          <div className="card p-8 mt-5">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
              <p className="text-base font-medium text-primary-dark">
                Processing Diagnosis...
              </p>
              <p className="text-sm text-primary-700 mt-2">
                Analyzing symptoms with AI models
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DiagnosisPage;
