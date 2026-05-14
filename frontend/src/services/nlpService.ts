/**
 * NLP Service for Real-Time Symptom Extraction
 * Processes free text and extracts medical symptoms
 */

import type { Symptom } from '@/types';

export class NLPService {
  private symptomList: string[] = [];
  private symptomMap: Map<string, string> = new Map();

  /**
   * Initialize with symptom list from backend
   */
  initialize(symptoms: Symptom[]) {
    this.symptomList = symptoms.map((s) => s.name.toLowerCase());
    
    // Create fuzzy matching map
    this.symptomList.forEach((symptom) => {
      this.symptomMap.set(symptom, symptom);
      // Add common variations
      this.symptomMap.set(symptom.replace(/\s+/g, ''), symptom);
    });
  }

  /**
   * Extract symptoms from free text in real-time
   */
  extractSymptoms(text: string): string[] {
    if (!text || text.trim().length === 0) return [];

    const normalizedText = text.toLowerCase();
    const extractedSymptoms = new Set<string>();

    // Direct matching
    this.symptomList.forEach((symptom) => {
      if (normalizedText.includes(symptom)) {
        extractedSymptoms.add(symptom);
      }
    });

    // Word-based matching for multi-word symptoms
    const words = normalizedText.split(/\s+/);
    for (let i = 0; i < words.length; i++) {
      // Try 1-word, 2-word, 3-word combinations
      for (let len = 1; len <= 3 && i + len <= words.length; len++) {
        const phrase = words.slice(i, i + len).join(' ');
        if (this.symptomList.includes(phrase)) {
          extractedSymptoms.add(phrase);
        }
      }
    }

    return Array.from(extractedSymptoms);
  }

  /**
   * Get symptom suggestions based on partial input
   */
  getSuggestions(input: string, limit: number = 10): string[] {
    if (!input || input.trim().length < 2) return [];

    const normalizedInput = input.toLowerCase().trim();
    const suggestions: string[] = [];

    // Exact prefix matches first
    this.symptomList.forEach((symptom) => {
      if (symptom.startsWith(normalizedInput)) {
        suggestions.push(symptom);
      }
    });

    // Contains matches
    if (suggestions.length < limit) {
      this.symptomList.forEach((symptom) => {
        if (!suggestions.includes(symptom) && symptom.includes(normalizedInput)) {
          suggestions.push(symptom);
        }
      });
    }

    // Fuzzy matches (simple Levenshtein-like)
    if (suggestions.length < limit) {
      this.symptomList.forEach((symptom) => {
        if (!suggestions.includes(symptom) && this.fuzzyMatch(normalizedInput, symptom)) {
          suggestions.push(symptom);
        }
      });
    }

    return suggestions.slice(0, limit);
  }

  /**
   * Simple fuzzy matching
   */
  private fuzzyMatch(input: string, target: string): boolean {
    if (input.length === 0) return false;
    
    let inputIndex = 0;
    for (let i = 0; i < target.length && inputIndex < input.length; i++) {
      if (target[i] === input[inputIndex]) {
        inputIndex++;
      }
    }
    
    return inputIndex === input.length;
  }

  /**
   * Merge checkbox and extracted symptoms, removing duplicates
   */
  mergeSymptoms(checkboxSymptoms: string[], extractedSymptoms: string[]): string[] {
    const merged = new Set<string>();
    
    // Add all checkbox symptoms
    checkboxSymptoms.forEach((s) => merged.add(s.toLowerCase()));
    
    // Add extracted symptoms
    extractedSymptoms.forEach((s) => merged.add(s.toLowerCase()));
    
    return Array.from(merged);
  }

  /**
   * Highlight symptoms in text
   */
  highlightSymptoms(text: string, symptoms: string[]): Array<{ text: string; isSymptom: boolean }> {
    if (!text || symptoms.length === 0) {
      return [{ text, isSymptom: false }];
    }

    const result: Array<{ text: string; isSymptom: boolean }> = [];
    let currentIndex = 0;
    const normalizedText = text.toLowerCase();

    // Sort symptoms by length (longest first) to match longer phrases first
    const sortedSymptoms = [...symptoms].sort((a, b) => b.length - a.length);

    const matches: Array<{ start: number; end: number; symptom: string }> = [];

    // Find all matches
    sortedSymptoms.forEach((symptom) => {
      let index = normalizedText.indexOf(symptom);
      while (index !== -1) {
        // Check if this position is not already covered
        const overlaps = matches.some(
          (m) => (index >= m.start && index < m.end) || (index + symptom.length > m.start && index < m.end)
        );
        
        if (!overlaps) {
          matches.push({
            start: index,
            end: index + symptom.length,
            symptom,
          });
        }
        
        index = normalizedText.indexOf(symptom, index + 1);
      }
    });

    // Sort matches by start position
    matches.sort((a, b) => a.start - b.start);

    // Build result array
    matches.forEach((match) => {
      // Add text before match
      if (currentIndex < match.start) {
        result.push({
          text: text.substring(currentIndex, match.start),
          isSymptom: false,
        });
      }
      
      // Add matched symptom
      result.push({
        text: text.substring(match.start, match.end),
        isSymptom: true,
      });
      
      currentIndex = match.end;
    });

    // Add remaining text
    if (currentIndex < text.length) {
      result.push({
        text: text.substring(currentIndex),
        isSymptom: false,
      });
    }

    return result.length > 0 ? result : [{ text, isSymptom: false }];
  }
}

// Singleton instance
export const nlpService = new NLPService();
