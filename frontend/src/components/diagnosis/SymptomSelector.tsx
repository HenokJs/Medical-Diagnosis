/**
 * Professional Symptom Selector
 * Searchable multi-select with categories
 */

import { useState, useEffect } from "react";
import { Search, X, Plus } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import diagnosisApi from "@/api/diagnosisApi";
import LoadingSpinner from "../common/LoadingSpinner";

interface SymptomSelectorProps {
  selectedSymptoms: string[];
  onSymptomsChange: (symptoms: string[]) => void;
}

const SymptomSelector = ({
  selectedSymptoms,
  onSymptomsChange,
}: SymptomSelectorProps) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredSymptoms, setFilteredSymptoms] = useState<string[]>([]);
  const [recentSymptoms, setRecentSymptoms] = useState<string[]>([]);

  // Fetch symptoms from API
  const { data: symptoms, isLoading } = useQuery({
    queryKey: ["symptoms"],
    queryFn: diagnosisApi.getSymptoms,
  });

  useEffect(() => {
    const stored = localStorage.getItem("recent_symptoms");
    if (stored) {
      try {
        const parsed = JSON.parse(stored) as string[];
        setRecentSymptoms(parsed);
      } catch {
        setRecentSymptoms([]);
      }
    }
  }, []);

  useEffect(() => {
    if (symptoms) {
      const filtered = symptoms
        .map((s) => s.name)
        .filter(
          (symptom) =>
            symptom.toLowerCase().includes(searchTerm.toLowerCase()) &&
            !selectedSymptoms.includes(symptom),
        )
        .slice(0, 10);
      setFilteredSymptoms(filtered);
    }
  }, [searchTerm, symptoms, selectedSymptoms]);

  const addSymptom = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom)) {
      onSymptomsChange([...selectedSymptoms, symptom]);
      setSearchTerm("");

      const updatedRecent = [
        symptom,
        ...recentSymptoms.filter((s) => s !== symptom),
      ].slice(0, 8);
      setRecentSymptoms(updatedRecent);
      localStorage.setItem("recent_symptoms", JSON.stringify(updatedRecent));
    }
  };

  const removeSymptom = (symptom: string) => {
    onSymptomsChange(selectedSymptoms.filter((s) => s !== symptom));
  };

  if (isLoading) {
    return (
      <div className="card p-6">
        <LoadingSpinner text="Loading symptoms..." />
      </div>
    );
  }

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Select Symptoms
      </h3>

      {/* Search Input */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search symptoms..."
          className="input pl-10"
        />
      </div>

      {/* Suggestions Dropdown */}
      {searchTerm && filteredSymptoms.length > 0 && (
        <div className="mb-4 border border-gray-200 rounded-lg max-h-48 overflow-y-auto custom-scrollbar">
          {filteredSymptoms.map((symptom) => (
            <button
              key={symptom}
              onClick={() => addSymptom(symptom)}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center justify-between group transition-colors"
            >
              <span className="text-sm text-gray-700">{symptom}</span>
              <Plus className="w-4 h-4 text-gray-400 group-hover:text-primary-600" />
            </button>
          ))}
        </div>
      )}

      {/* Selected Symptoms */}
      <div>
        <p className="text-sm font-medium text-gray-700 mb-2">
          Selected Symptoms ({selectedSymptoms.length})
        </p>
        {selectedSymptoms.length === 0 ? (
          <p className="text-sm text-gray-500 italic">
            No symptoms selected yet
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {selectedSymptoms.map((symptom) => (
              <span
                key={symptom}
                className="inline-flex items-center px-3 py-1.5 rounded-lg bg-primary-50 text-primary-700 text-sm font-medium"
              >
                {symptom}
                <button
                  onClick={() => removeSymptom(symptom)}
                  className="ml-2 hover:text-primary-900 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Recently Used */}
      {recentSymptoms.length > 0 && (
        <div className="mt-6">
          <p className="text-sm font-medium text-gray-700 mb-2">
            Recently Used
          </p>
          <div className="flex flex-wrap gap-2">
            {recentSymptoms
              .filter((symptom) => !selectedSymptoms.includes(symptom))
              .map((symptom) => (
                <button
                  key={symptom}
                  type="button"
                  onClick={() => addSymptom(symptom)}
                  className="inline-flex items-center px-3 py-1.5 rounded-lg bg-gray-100 text-gray-700 text-sm font-medium hover:bg-gray-200 transition-colors"
                >
                  {symptom}
                </button>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SymptomSelector;
