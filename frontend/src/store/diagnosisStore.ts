/**
 * Diagnosis State Management
 * Using Zustand for lightweight state management
 */

import { create } from "zustand";
import type { DiagnosisResponse, DiagnosisHistory, PatientInfo } from "@/types";

interface DiagnosisStore {
  // Current diagnosis state
  currentDiagnosis: DiagnosisResponse | null;
  selectedSymptoms: string[];
  patientInfo: PatientInfo | null;

  // History
  diagnosisHistory: DiagnosisHistory[];

  // UI state
  isLoading: boolean;
  error: string | null;

  // Actions
  setSelectedSymptoms: (symptoms: string[]) => void;
  addSymptom: (symptom: string) => void;
  removeSymptom: (symptom: string) => void;
  clearSymptoms: () => void;

  setPatientInfo: (info: PatientInfo) => void;

  setCurrentDiagnosis: (diagnosis: DiagnosisResponse) => void;
  addToHistory: (diagnosis: DiagnosisResponse) => void;
  clearHistory: () => void;

  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  reset: () => void;
}

export const useDiagnosisStore = create<DiagnosisStore>((set) => ({
  // Initial state
  currentDiagnosis: null,
  selectedSymptoms: [],
  patientInfo: null,
  diagnosisHistory: [],
  isLoading: false,
  error: null,

  // Symptom actions
  setSelectedSymptoms: (symptoms) => set({ selectedSymptoms: symptoms }),

  addSymptom: (symptom) =>
    set((state) => ({
      selectedSymptoms: [...new Set([...state.selectedSymptoms, symptom])],
    })),

  removeSymptom: (symptom) =>
    set((state) => ({
      selectedSymptoms: state.selectedSymptoms.filter((s) => s !== symptom),
    })),

  clearSymptoms: () => set({ selectedSymptoms: [] }),

  // Patient info actions
  setPatientInfo: (info) => set({ patientInfo: info }),

  // Diagnosis actions
  setCurrentDiagnosis: (diagnosis) => set({ currentDiagnosis: diagnosis }),

  addToHistory: (diagnosis) =>
    set((state) => {
      const topPrediction = diagnosis.data.top_predictions?.[0];
      const matchedSymptoms =
        diagnosis.data.explainability?.matched_symptoms || [];

      const historyItem: DiagnosisHistory = {
        id: Date.now().toString(),
        timestamp: diagnosis.timestamp,
        symptoms: matchedSymptoms,
        topPrediction: topPrediction?.disease || "Unknown",
        confidence: topPrediction?.confidence || 0,
        diagnosis,
        patientInfo: state.patientInfo || undefined,
      };

      return {
        diagnosisHistory: [historyItem, ...state.diagnosisHistory].slice(0, 10),
      };
    }),

  clearHistory: () => set({ diagnosisHistory: [] }),

  // UI state actions
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),

  // Reset all state
  reset: () =>
    set({
      currentDiagnosis: null,
      selectedSymptoms: [],
      patientInfo: null,
      isLoading: false,
      error: null,
    }),
}));
