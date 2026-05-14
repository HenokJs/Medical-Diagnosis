/**
 * Working Symptom Input Component
 * Combines checkbox selection + NLP extraction
 */

import { useState, useEffect, useMemo } from 'react';
import { Search, X, Sparkles, CheckCircle2, Plus, AlertCircle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import diagnosisApi from '@/api/diagnosisApi';

interface WorkingSymptomInputProps {
  selectedSymptoms: string[];
  onSymptomsChange: (symptoms: string[]) => void;
  freeText: string;
  onFreeTextChange: (text: string) => void;
}

const WorkingSymptomInput = ({
  selectedSymptoms,
  onSymptomsChange,
  freeText,
  onFreeTextChange,
}: WorkingSymptomInputProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Fetch symptoms from API
  const { data: symptomsData, isLoading, isError } = useQuery({
    queryKey: ['symptoms'],
    queryFn: diagnosisApi.getSymptoms,
    staleTime: 10 * 60 * 1000, // Cache for 10 minutes
  });

  const allSymptoms = useMemo(() => {
    return symptomsData?.map((s) => s.name) || [];
  }, [symptomsData]);

  // Filter symptoms based on search with improved matching
  const filteredSymptoms = useMemo(() => {
    if (searchTerm.length < 2) return [];

    const searchLower = searchTerm.toLowerCase().trim();
    
    return allSymptoms
      .filter((symptom) => {
        const symptomLower = symptom.toLowerCase();
        // Check if already selected
        if (selectedSymptoms.includes(symptom)) return false;
        
        // Exact match or starts with
        if (symptomLower.startsWith(searchLower)) return true;
        
        // Contains match
        if (symptomLower.includes(searchLower)) return true;
        
        // Word boundary match
        const words = symptomLower.split(/\s+/);
        return words.some(word => word.startsWith(searchLower));
      })
      .slice(0, 10);
  }, [searchTerm, allSymptoms, selectedSymptoms]);

  // Extract symptoms from free text with improved detection
  const extractedSymptoms = useMemo(() => {
    if (!freeText || freeText.length < 3 || allSymptoms.length === 0) {
      return [];
    }

    const text = freeText.toLowerCase();
    const detected = new Set<string>();

    // Sort symptoms by length (longest first) to match longer phrases first
    const sortedSymptoms = [...allSymptoms].sort((a, b) => b.length - a.length);

    sortedSymptoms.forEach((symptom) => {
      const symptomLower = symptom.toLowerCase();
      
      // Direct substring match
      if (text.includes(symptomLower)) {
        detected.add(symptom);
        return;
      }
      
      // Word boundary match for multi-word symptoms
      const symptomWords = symptomLower.split(/\s+/);
      if (symptomWords.length > 1) {
        const regex = new RegExp(`\\b${symptomWords.join('\\s+')}\\b`, 'i');
        if (regex.test(text)) {
          detected.add(symptom);
        }
      }
    });

    return Array.from(detected);
  }, [freeText, allSymptoms]);

  const addSymptom = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom)) {
      onSymptomsChange([...selectedSymptoms, symptom]);
      setSearchTerm('');
      setShowSuggestions(false);
    }
  };

  const removeSymptom = (symptom: string) => {
    onSymptomsChange(selectedSymptoms.filter((s) => s !== symptom));
  };

  const handleSearchChange = (value: string) => {
    setSearchTerm(value);
    setShowSuggestions(value.length >= 2);
  };

  const handleSearchFocus = () => {
    if (searchTerm.length >= 2) {
      setShowSuggestions(true);
    }
  };

  const handleSearchBlur = () => {
    // Delay to allow click on suggestion
    setTimeout(() => setShowSuggestions(false), 200);
  };

  // Count pending symptoms (extracted but not selected)
  const pendingSymptoms = extractedSymptoms.filter(s => !selectedSymptoms.includes(s));

  return (
    <div className="space-y-4">
      {/* Loading State */}
      {isLoading && (
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <p className="text-sm text-blue-800">Loading symptoms...</p>
          </div>
        </div>
      )}

      {/* Error State */}
      {isError && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-sm text-red-800">
              Failed to load symptoms. Please refresh the page.
            </p>
          </div>
        </div>
      )}

      {/* Free Text Input */}
      <div className="bg-white rounded-lg border-2 border-[#0077b6] p-5 shadow-sm">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-5 h-5 text-[#0077b6]" />
          <h3 className="text-base font-semibold text-[#03045e]">
            Describe Symptoms (AI-Powered)
          </h3>
        </div>

        <textarea
          value={freeText}
          onChange={(e) => onFreeTextChange(e.target.value)}
          placeholder="Example: I have fever, chest pain, and difficulty breathing..."
          rows={4}
          disabled={isLoading}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-[#0077b6] text-sm transition-colors disabled:bg-gray-50 disabled:cursor-not-allowed"
        />

        {/* Extracted Symptoms */}
        {extractedSymptoms.length > 0 && (
          <div className="mt-3 p-3 bg-[#caf0f8] rounded-lg">
            <p className="text-xs font-semibold text-[#03045e] mb-2">
              ✨ AI Detected ({extractedSymptoms.length})
            </p>
            <div className="flex flex-wrap gap-2">
              {extractedSymptoms.map((symptom) => {
                const isSelected = selectedSymptoms.includes(symptom);
                return (
                  <button
                    key={symptom}
                    type="button"
                    onClick={() => !isSelected && addSymptom(symptom)}
                    disabled={isSelected}
                    className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      isSelected
                        ? 'bg-[#00b4d8] text-white cursor-default'
                        : 'bg-white text-[#0077b6] border-2 border-[#00b4d8] hover:bg-[#90e0ef] cursor-pointer'
                    }`}
                  >
                    {isSelected && <CheckCircle2 className="w-3.5 h-3.5 mr-1" />}
                    {symptom}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Search & Select */}
      <div className="bg-white rounded-lg border-2 border-gray-200 p-5 shadow-sm">
        <h3 className="text-base font-semibold text-[#03045e] mb-3">
          Search & Select Symptoms
        </h3>

        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => handleSearchChange(e.target.value)}
            onFocus={handleSearchFocus}
            onBlur={handleSearchBlur}
            placeholder="Type to search symptoms..."
            disabled={isLoading}
            className="w-full pl-10 pr-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-[#0077b6] text-sm transition-colors disabled:bg-gray-50 disabled:cursor-not-allowed"
          />
        </div>

        {/* Suggestions Dropdown */}
        {showSuggestions && filteredSymptoms.length > 0 && (
          <div className="mb-4 border-2 border-[#0077b6] rounded-lg max-h-48 overflow-y-auto shadow-lg">
            {filteredSymptoms.map((symptom) => (
              <button
                key={symptom}
                type="button"
                onClick={() => addSymptom(symptom)}
                className="w-full px-4 py-2.5 text-left hover:bg-[#caf0f8] flex items-center justify-between group transition-colors text-sm border-b border-gray-100 last:border-b-0"
              >
                <span className="text-gray-700 font-medium">{symptom}</span>
                <Plus className="w-4 h-4 text-gray-400 group-hover:text-[#0077b6] transition-colors" />
              </button>
            ))}
          </div>
        )}

        {/* No results message */}
        {searchTerm.length >= 2 && filteredSymptoms.length === 0 && !isLoading && (
          <div className="mb-4 p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-sm text-gray-600">No symptoms found matching "{searchTerm}"</p>
          </div>
        )}

        {/* Selected Symptoms */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-semibold text-gray-600">
              Selected ({selectedSymptoms.length})
            </p>
            {selectedSymptoms.length > 0 && (
              <button
                type="button"
                onClick={() => onSymptomsChange([])}
                className="text-xs text-red-600 hover:text-red-700 font-medium transition-colors"
              >
                Clear All
              </button>
            )}
          </div>

          {selectedSymptoms.length === 0 ? (
            <p className="text-sm text-gray-500 italic py-2">No symptoms selected yet</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {selectedSymptoms.map((symptom) => (
                <span
                  key={symptom}
                  className="inline-flex items-center px-3 py-1.5 rounded-lg bg-[#03045e] text-white text-sm font-medium"
                >
                  {symptom}
                  <button
                    type="button"
                    onClick={() => removeSymptom(symptom)}
                    className="ml-2 hover:bg-[#0077b6] rounded-full p-0.5 transition-colors"
                    aria-label={`Remove ${symptom}`}
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Summary */}
      <div className="bg-gradient-to-r from-[#caf0f8] to-[#90e0ef] border-2 border-[#00b4d8] rounded-lg p-4">
        <div className="flex items-start gap-3">
          <Sparkles className="w-5 h-5 text-[#03045e] flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-[#03045e] mb-1">
              Ready to Analyze: {selectedSymptoms.length} symptom{selectedSymptoms.length !== 1 ? 's' : ''}
            </p>
            <p className="text-xs text-[#03045e]">
              {selectedSymptoms.length} manually selected
              {extractedSymptoms.length > 0 && ` • ${extractedSymptoms.length} AI-detected`}
              {pendingSymptoms.length > 0 && 
                ` • ${pendingSymptoms.length} pending (click to add)`}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkingSymptomInput;
