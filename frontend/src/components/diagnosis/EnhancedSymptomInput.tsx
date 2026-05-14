/**
 * Enhanced Symptom Input with Real-Time NLP
 * Professional medical-grade symptom capture
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, X, Sparkles, CheckCircle2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import diagnosisApi from '@/api/diagnosisApi';
import { nlpService } from '@/services/nlpService';
import { debounce } from '@/utils/helpers';

interface EnhancedSymptomInputProps {
  selectedSymptoms: string[];
  onSymptomsChange: (symptoms: string[]) => void;
  freeText: string;
  onFreeTextChange: (text: string) => void;
}

const EnhancedSymptomInput = ({
  selectedSymptoms,
  onSymptomsChange,
  freeText,
  onFreeTextChange,
}: EnhancedSymptomInputProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [extractedSymptoms, setExtractedSymptoms] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedText, setHighlightedText] = useState<Array<{ text: string; isSymptom: boolean }>>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Fetch symptoms from API
  const { data: symptoms } = useQuery({
    queryKey: ['symptoms'],
    queryFn: diagnosisApi.getSymptoms,
  });

  // Initialize NLP service
  useEffect(() => {
    if (symptoms) {
      nlpService.initialize(symptoms);
    }
  }, [symptoms]);

  // Extract symptoms from free text in real-time
  const extractSymptomsFromText = useCallback(
    debounce((text: string) => {
      if (!text || text.trim().length === 0) {
        setExtractedSymptoms([]);
        setHighlightedText([]);
        return;
      }

      const extracted = nlpService.extractSymptoms(text);
      setExtractedSymptoms(extracted);
      
      // Highlight symptoms in text
      const highlighted = nlpService.highlightSymptoms(text, extracted);
      setHighlightedText(highlighted);
    }, 300),
    []
  );

  // Handle free text change
  const handleFreeTextChange = (text: string) => {
    onFreeTextChange(text);
    extractSymptomsFromText(text);
  };

  // Get suggestions for search
  const updateSuggestions = useCallback(
    debounce((term: string) => {
      if (term.length < 2) {
        setSuggestions([]);
        return;
      }

      const filtered = nlpService.getSuggestions(term, 8);
      const available = filtered.filter((s) => !selectedSymptoms.includes(s));
      setSuggestions(available);
    }, 200),
    [selectedSymptoms]
  );

  useEffect(() => {
    updateSuggestions(searchTerm);
  }, [searchTerm, updateSuggestions]);

  // Add symptom
  const addSymptom = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom)) {
      onSymptomsChange([...selectedSymptoms, symptom]);
      setSearchTerm('');
      setSuggestions([]);
    }
  };

  // Remove symptom
  const removeSymptom = (symptom: string) => {
    onSymptomsChange(selectedSymptoms.filter((s) => s !== symptom));
  };

  // Add extracted symptom to selected
  const addExtractedSymptom = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom)) {
      onSymptomsChange([...selectedSymptoms, symptom]);
    }
  };

  // Get merged symptoms count
  const mergedSymptoms = nlpService.mergeSymptoms(selectedSymptoms, extractedSymptoms);
  const totalSymptoms = mergedSymptoms.length;

  return (
    <div className="space-y-4">
      {/* Free Text Input with NLP */}
      <div className="card p-5">
        <div className="flex items-center space-x-2 mb-3">
          <Sparkles className="w-5 h-5 text-primary-600" />
          <h3 className="text-base font-semibold text-gray-900">
            Describe Symptoms (AI-Powered)
          </h3>
        </div>

        <div className="relative">
          <textarea
            ref={textareaRef}
            value={freeText}
            onChange={(e) => handleFreeTextChange(e.target.value)}
            placeholder="Example: I have fever, chest pain, and difficulty breathing for 3 days..."
            rows={4}
            className="input resize-none text-sm"
          />
          
          {/* Character count */}
          <div className="absolute bottom-2 right-2 text-xs text-gray-400">
            {freeText.length} / 500
          </div>
        </div>

        {/* Highlighted text preview (optional) */}
        {highlightedText.length > 0 && freeText.length > 0 && (
          <div className="mt-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-medium text-gray-600 mb-2">AI Recognition:</p>
            <div className="text-sm leading-relaxed">
              {highlightedText.map((segment, index) => (
                <span
                  key={index}
                  className={
                    segment.isSymptom
                      ? 'bg-primary-100 text-primary-800 px-1 rounded font-medium'
                      : 'text-gray-700'
                  }
                >
                  {segment.text}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Extracted Symptoms */}
        {extractedSymptoms.length > 0 && (
          <div className="mt-3">
            <p className="text-xs font-medium text-gray-600 mb-2">
              Detected Symptoms ({extractedSymptoms.length})
            </p>
            <div className="flex flex-wrap gap-2">
              {extractedSymptoms.map((symptom) => {
                const isSelected = selectedSymptoms.includes(symptom);
                return (
                  <button
                    key={symptom}
                    onClick={() => !isSelected && addExtractedSymptom(symptom)}
                    disabled={isSelected}
                    className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      isSelected
                        ? 'bg-green-100 text-green-800 border border-green-300 cursor-default'
                        : 'bg-primary-50 text-primary-700 border border-primary-200 hover:bg-primary-100 cursor-pointer'
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

      {/* Manual Symptom Search */}
      <div className="card p-5">
        <h3 className="text-base font-semibold text-gray-900 mb-3">
          Search & Select Symptoms
        </h3>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onFocus={() => setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            placeholder="Search symptoms..."
            className="input pl-10 text-sm"
          />
        </div>

        {/* Suggestions Dropdown */}
        {showSuggestions && suggestions.length > 0 && (
          <div className="mt-2 border border-gray-200 rounded-lg max-h-48 overflow-y-auto bg-white shadow-sm">
            {suggestions.map((symptom) => (
              <button
                key={symptom}
                onClick={() => addSymptom(symptom)}
                className="w-full px-4 py-2.5 text-left hover:bg-gray-50 flex items-center justify-between group transition-colors text-sm"
              >
                <span className="text-gray-700">{symptom}</span>
                <span className="text-xs text-gray-400 group-hover:text-primary-600">
                  Add
                </span>
              </button>
            ))}
          </div>
        )}

        {/* Selected Symptoms */}
        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-medium text-gray-600">
              Selected Symptoms ({selectedSymptoms.length})
            </p>
            {selectedSymptoms.length > 0 && (
              <button
                onClick={() => onSymptomsChange([])}
                className="text-xs text-red-600 hover:text-red-700 font-medium"
              >
                Clear All
              </button>
            )}
          </div>

          {selectedSymptoms.length === 0 ? (
            <p className="text-sm text-gray-500 italic py-2">No symptoms selected</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {selectedSymptoms.map((symptom) => (
                <span
                  key={symptom}
                  className="inline-flex items-center px-3 py-1.5 rounded-lg bg-primary-600 text-white text-sm font-medium"
                >
                  {symptom}
                  <button
                    onClick={() => removeSymptom(symptom)}
                    className="ml-2 hover:bg-primary-700 rounded-full p-0.5 transition-colors"
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
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Sparkles className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-blue-900 mb-1">
              Total Symptoms for Analysis: {totalSymptoms}
            </p>
            <p className="text-xs text-blue-700">
              {selectedSymptoms.length} manually selected • {extractedSymptoms.length} AI-detected
              {extractedSymptoms.length > 0 && ` • ${extractedSymptoms.filter(s => !selectedSymptoms.includes(s)).length} pending confirmation`}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedSymptomInput;
