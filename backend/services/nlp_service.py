"""
NLP Service
===========
Natural Language Processing for symptom extraction with fuzzy matching.

Author: Senior Backend Engineer
Date: 2026-05-11
Updated: 2026-05-12 - Added fuzzy matching and confidence scoring
"""

import re
from typing import List, Set, Dict, Tuple
import logging
from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)


class NLPService:
    """
    Enhanced NLP service for processing free-text symptoms.
    
    Features:
    - Symptom extraction from text
    - Fuzzy matching for typo tolerance
    - Synonym mapping
    - Confidence scoring
    - Source tracking (checkbox vs NLP)
    """
    
    def __init__(self):
        """Initialize NLP service."""
        self._initialize_symptom_keywords()
        self._initialize_synonyms()
        self._initialize_all_symptoms()
        logger.info("Enhanced NLP service initialized with fuzzy matching")
    
    def _initialize_symptom_keywords(self):
        """Initialize common symptom keywords."""
        self.symptom_keywords = {
            'fever': ['fever', 'temperature', 'hot', 'burning up', 'feverish', 'pyrexia'],
            'cough': ['cough', 'coughing', 'hacking', 'persistent cough'],
            'headache': ['headache', 'head pain', 'head ache', 'migraine', 'cephalalgia'],
            'fatigue': ['fatigue', 'tired', 'exhausted', 'weakness', 'weak', 'lethargy', 'tiredness'],
            'nausea': ['nausea', 'nauseous', 'sick', 'queasy', 'feeling sick'],
            'vomiting': ['vomiting', 'throwing up', 'vomit', 'puking', 'emesis'],
            'diarrhea': ['diarrhea', 'loose stools', 'watery stools', 'diarrhoea'],
            'abdominal pain': ['stomach ache', 'belly pain', 'abdominal pain', 'stomach pain', 'tummy ache'],
            'chest pain': ['chest pain', 'chest discomfort', 'chest pressure', 'angina'],
            'shortness of breath': ['shortness of breath', 'breathing difficulty', 'breathless', 'cant breathe', 'dyspnea', 'difficulty breathing'],
            'sore throat': ['sore throat', 'throat pain', 'painful throat', 'pharyngitis'],
            'body pain': ['body ache', 'body pain', 'muscle pain', 'aching', 'myalgia'],
            'chills': ['chills', 'shivering', 'cold', 'rigors'],
            'sweating': ['sweating', 'perspiring', 'night sweats', 'diaphoresis'],
            'dizziness': ['dizzy', 'dizziness', 'lightheaded', 'vertigo'],
            'rash': ['rash', 'skin rash', 'skin eruption', 'hives'],
            'itching': ['itching', 'itchy', 'scratching', 'pruritus'],
            'joint pain': ['joint pain', 'arthralgia', 'joint ache'],
            'back pain': ['back pain', 'backache', 'lower back pain'],
            'neck pain': ['neck pain', 'stiff neck', 'neck stiffness'],
            'nasal congestion': ['runny nose', 'stuffy nose', 'blocked nose', 'nasal congestion', 'congestion'],
            'sneezing': ['sneezing', 'sneeze'],
            'loss of appetite': ['loss of appetite', 'no appetite', 'not hungry', 'anorexia'],
            'weight loss': ['weight loss', 'losing weight', 'lost weight'],
            'confusion': ['confusion', 'confused', 'disoriented', 'mental confusion'],
            'anxiety': ['anxiety', 'anxious', 'worried', 'nervous'],
            'insomnia': ['insomnia', 'cant sleep', 'sleeplessness', 'trouble sleeping'],
        }
    
    def _initialize_synonyms(self):
        """Initialize symptom synonyms."""
        self.synonyms = {
            'high temperature': 'fever',
            'elevated temperature': 'fever',
            'running a fever': 'fever',
            'feeling hot': 'fever',
            'stomach ache': 'abdominal pain',
            'tummy ache': 'abdominal pain',
            'belly ache': 'abdominal pain',
            'feeling sick': 'nausea',
            'feeling nauseous': 'nausea',
            'throwing up': 'vomiting',
            'being sick': 'vomiting',
            'runny nose': 'nasal congestion',
            'stuffy nose': 'nasal congestion',
            'blocked nose': 'nasal congestion',
            'cant breathe': 'shortness of breath',
            'difficulty breathing': 'shortness of breath',
            'short of breath': 'shortness of breath',
            'muscle ache': 'body pain',
            'muscle pain': 'body pain',
            'aching muscles': 'body pain',
        }
    
    def _initialize_all_symptoms(self):
        """Create a flat list of all known symptoms for fuzzy matching."""
        self.all_known_symptoms = set()
        for symptom, keywords in self.symptom_keywords.items():
            self.all_known_symptoms.add(symptom)
            self.all_known_symptoms.update(keywords)
        self.all_known_symptoms.update(self.synonyms.keys())
    
    def fuzzy_match_symptom(self, text: str, threshold: int = 80) -> Tuple[str, float]:
        """
        Fuzzy match a symptom with typo tolerance.
        
        Args:
            text: Input text to match
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Tuple of (matched_symptom, confidence_score)
        """
        if not text:
            return None, 0.0
        
        text_clean = text.lower().strip()
        
        # Try exact match first
        if text_clean in self.all_known_symptoms:
            return text_clean, 1.0
        
        # Fuzzy match
        result = process.extractOne(
            text_clean,
            self.all_known_symptoms,
            scorer=fuzz.ratio,
            score_cutoff=threshold
        )
        
        if result:
            matched_text, score, _ = result
            confidence = score / 100.0
            logger.debug(f"Fuzzy matched '{text}' to '{matched_text}' (confidence: {confidence:.2f})")
            return matched_text, confidence
        
        return None, 0.0
    
    def extract_symptoms_with_confidence(self, text: str) -> List[Dict]:
        """
        Extract symptoms from free text with confidence scores.
        
        Args:
            text: Free-text symptom description
            
        Returns:
            List of dicts with {symptom, confidence, source}
        """
        if not text:
            return []
        
        # Normalize text
        text_lower = text.lower().strip()
        text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
        
        extracted = {}
        
        # Split into potential symptom phrases
        phrases = self._extract_phrases(text_clean)
        
        for phrase in phrases:
            # Try exact keyword match first
            matched = False
            for symptom, keywords in self.symptom_keywords.items():
                for keyword in keywords:
                    if keyword in phrase:
                        if symptom not in extracted or extracted[symptom]['confidence'] < 1.0:
                            extracted[symptom] = {
                                'symptom': symptom,
                                'confidence': 1.0,
                                'source': 'nlp_exact',
                                'original_text': phrase
                            }
                        matched = True
                        break
                if matched:
                    break
            
            # Try synonym match
            if not matched:
                for synonym, symptom in self.synonyms.items():
                    if synonym in phrase:
                        if symptom not in extracted or extracted[symptom]['confidence'] < 0.95:
                            extracted[symptom] = {
                                'symptom': symptom,
                                'confidence': 0.95,
                                'source': 'nlp_synonym',
                                'original_text': phrase
                            }
                        matched = True
                        break
            
            # Try fuzzy match for typos
            if not matched and len(phrase.split()) <= 3:  # Only fuzzy match short phrases
                matched_symptom, confidence = self.fuzzy_match_symptom(phrase, threshold=75)
                if matched_symptom and confidence >= 0.75:
                    # Normalize to standard symptom
                    standard_symptom = self._normalize_to_standard(matched_symptom)
                    if standard_symptom not in extracted or extracted[standard_symptom]['confidence'] < confidence:
                        extracted[standard_symptom] = {
                            'symptom': standard_symptom,
                            'confidence': confidence,
                            'source': 'nlp_fuzzy',
                            'original_text': phrase
                        }
        
        return list(extracted.values())
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract potential symptom phrases from text."""
        # Split by common separators
        separators = [' and ', ' or ', ',', ';', '\n']
        phrases = [text]
        
        for sep in separators:
            new_phrases = []
            for phrase in phrases:
                new_phrases.extend(phrase.split(sep))
            phrases = new_phrases
        
        # Clean and filter
        phrases = [p.strip() for p in phrases if p.strip()]
        
        # Also include the full text for multi-word symptoms
        phrases.append(text)
        
        return phrases
    
    def _normalize_to_standard(self, matched_text: str) -> str:
        """Normalize a matched text to standard symptom name."""
        # Check if it's a synonym
        if matched_text in self.synonyms:
            return self.synonyms[matched_text]
        
        # Check if it's a keyword
        for symptom, keywords in self.symptom_keywords.items():
            if matched_text in keywords:
                return symptom
        
        return matched_text
    
    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract symptoms from free text (simple version).
        
        Args:
            text: Free-text symptom description
            
        Returns:
            List of extracted symptoms
        """
        results = self.extract_symptoms_with_confidence(text)
        return [r['symptom'] for r in results if r['confidence'] >= 0.7]
    
    def normalize_symptom(self, symptom: str) -> str:
        """
        Normalize a single symptom.
        
        Args:
            symptom: Symptom text
            
        Returns:
            Normalized symptom
        """
        symptom_lower = symptom.lower().strip()
        
        # Check synonyms
        if symptom_lower in self.synonyms:
            return self.synonyms[symptom_lower]
        
        # Check if it matches any keyword
        for standard_symptom, keywords in self.symptom_keywords.items():
            if symptom_lower in keywords:
                return standard_symptom
        
        # Try fuzzy match
        matched, confidence = self.fuzzy_match_symptom(symptom_lower, threshold=85)
        if matched and confidence >= 0.85:
            return self._normalize_to_standard(matched)
        
        return symptom_lower
    
    def process_input(self, structured_symptoms: List[str] = None,
                     free_text: str = None) -> List[str]:
        """
        Process both structured and free-text symptom input.
        
        Args:
            structured_symptoms: List of structured symptoms
            free_text: Free-text symptom description
            
        Returns:
            Combined and normalized symptom list
        """
        all_symptoms = set()
        
        # Process structured symptoms
        if structured_symptoms:
            for symptom in structured_symptoms:
                normalized = self.normalize_symptom(symptom)
                all_symptoms.add(normalized)
        
        # Process free text
        if free_text:
            extracted = self.extract_symptoms(free_text)
            all_symptoms.update(extracted)
        
        return list(all_symptoms)
    
    def process_input_detailed(self, structured_symptoms: List[str] = None,
                              free_text: str = None) -> Dict:
        """
        Process input with detailed extraction information.
        
        Args:
            structured_symptoms: List of structured symptoms
            free_text: Free-text symptom description
            
        Returns:
            Dict with detailed extraction info
        """
        result = {
            'structured': [],
            'extracted': [],
            'merged': [],
            'all_symptoms': []
        }
        
        # Process structured symptoms
        if structured_symptoms:
            for symptom in structured_symptoms:
                normalized = self.normalize_symptom(symptom)
                result['structured'].append({
                    'original': symptom,
                    'normalized': normalized,
                    'source': 'checkbox',
                    'confidence': 1.0
                })
        
        # Process free text
        if free_text:
            extracted = self.extract_symptoms_with_confidence(free_text)
            result['extracted'] = extracted
        
        # Merge and deduplicate
        all_symptoms = set()
        merged = []
        
        for item in result['structured']:
            all_symptoms.add(item['normalized'])
            merged.append(item)
        
        for item in result['extracted']:
            if item['symptom'] not in all_symptoms:
                all_symptoms.add(item['symptom'])
                merged.append({
                    'original': item['original_text'],
                    'normalized': item['symptom'],
                    'source': item['source'],
                    'confidence': item['confidence']
                })
        
        result['merged'] = merged
        result['all_symptoms'] = list(all_symptoms)
        
        return result
    
    def get_symptom_suggestions(self, partial: str, max_suggestions: int = 5) -> List[str]:
        """
        Get symptom suggestions for autocomplete.
        
        Args:
            partial: Partial symptom text
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of symptom suggestions
        """
        if not partial:
            return []
        
        partial_lower = partial.lower().strip()
        suggestions = set()
        
        # Exact prefix match
        for symptom in self.symptom_keywords.keys():
            if symptom.startswith(partial_lower):
                suggestions.add(symptom)
        
        # Fuzzy match
        if len(suggestions) < max_suggestions:
            fuzzy_results = process.extract(
                partial_lower,
                self.symptom_keywords.keys(),
                scorer=fuzz.partial_ratio,
                limit=max_suggestions
            )
            for symptom, score, _ in fuzzy_results:
                if score >= 70:
                    suggestions.add(symptom)
        
        return list(suggestions)[:max_suggestions]


# Global singleton instance
nlp_service = NLPService()
