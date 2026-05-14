/**
 * Symptom Highlighter Component
 * Displays extracted symptoms with confidence scores and sources
 */

import { CheckCircle, Sparkles, AlertCircle } from 'lucide-react';

interface ExtractedSymptom {
  original: string;
  normalized: string;
  source: string;
  confidence: number;
}

interface SymptomHighlighterProps {
  symptoms: ExtractedSymptom[];
  className?: string;
}

const SymptomHighlighter = ({ symptoms, className = '' }: SymptomHighlighterProps) => {
  if (!symptoms || symptoms.length === 0) {
    return null;
  }

  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'checkbox':
        return <CheckCircle className="w-3 h-3" />;
      case 'nlp_exact':
      case 'nlp_synonym':
        return <Sparkles className="w-3 h-3" />;
      case 'nlp_fuzzy':
        return <AlertCircle className="w-3 h-3" />;
      default:
        return <CheckCircle className="w-3 h-3" />;
    }
  };

  const getSourceLabel = (source: string) => {
    switch (source) {
      case 'checkbox':
        return 'Selected';
      case 'nlp_exact':
        return 'Extracted';
      case 'nlp_synonym':
        return 'Synonym';
      case 'nlp_fuzzy':
        return 'Fuzzy Match';
      default:
        return 'Detected';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.95) return 'bg-green-50 border-green-300 text-green-800';
    if (confidence >= 0.85) return 'bg-blue-50 border-blue-300 text-blue-800';
    if (confidence >= 0.75) return 'bg-amber-50 border-amber-300 text-amber-800';
    return 'bg-orange-50 border-orange-300 text-orange-800';
  };

  return (
    <div className={`card p-4 ${className}`}>
      <h4 className="text-sm font-semibold text-neutral-700 mb-3 flex items-center">
        <Sparkles className="w-4 h-4 mr-2 text-primary-blue" />
        Detected Symptoms ({symptoms.length})
      </h4>
      
      <div className="flex flex-wrap gap-2">
        {symptoms.map((symptom, index) => (
          <div
            key={index}
            className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-200 ${getConfidenceColor(symptom.confidence)}`}
            title={`Source: ${getSourceLabel(symptom.source)} | Confidence: ${(symptom.confidence * 100).toFixed(0)}%`}
          >
            <span className="mr-1.5">{getSourceIcon(symptom.source)}</span>
            <span className="font-semibold">{symptom.normalized}</span>
            {symptom.confidence < 1.0 && (
              <span className="ml-1.5 opacity-75">
                ({(symptom.confidence * 100).toFixed(0)}%)
              </span>
            )}
          </div>
        ))}
      </div>

      <div className="mt-3 pt-3 border-t border-neutral-200">
        <div className="flex items-center gap-4 text-xs text-neutral-600">
          <div className="flex items-center gap-1">
            <CheckCircle className="w-3 h-3 text-green-600" />
            <span>Selected</span>
          </div>
          <div className="flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-blue-600" />
            <span>AI Extracted</span>
          </div>
          <div className="flex items-center gap-1">
            <AlertCircle className="w-3 h-3 text-amber-600" />
            <span>Fuzzy Match</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SymptomHighlighter;
