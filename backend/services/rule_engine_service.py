"""
Rule Engine Service
===================
Clinical rule-based reasoning engine.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)


class ClinicalRule:
    """Represents a clinical decision rule."""
    
    def __init__(self, rule_id: str, name: str, conditions: List[str],
                 action: str, priority: str, category: str, explanation: str):
        """
        Initialize clinical rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Rule name
            conditions: List of required symptoms
            action: Action/flag to raise
            priority: Priority level (low, medium, high, critical)
            category: Rule category
            explanation: Human-readable explanation
        """
        self.rule_id = rule_id
        self.name = name
        self.conditions = [c.lower().strip() for c in conditions]
        self.action = action
        self.priority = priority
        self.category = category
        self.explanation = explanation
    
    def evaluate(self, symptoms: Set[str]) -> bool:
        """
        Evaluate if rule conditions are met.
        
        Args:
            symptoms: Set of patient symptoms
            
        Returns:
            True if all conditions met
        """
        symptoms_lower = {s.lower().strip() for s in symptoms}
        return all(condition in symptoms_lower for condition in self.conditions)
    
    def to_dict(self) -> Dict:
        """Convert rule to dictionary."""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'action': self.action,
            'priority': self.priority,
            'category': self.category,
            'explanation': self.explanation,
            'triggered_by': self.conditions
        }


class RuleEngineService:
    """
    Clinical rule engine for hybrid AI diagnosis.
    
    Implements rule-based clinical logic to complement ML predictions.
    """
    
    def __init__(self):
        """Initialize rule engine with clinical rules."""
        self.rules: List[ClinicalRule] = []
        self._initialize_rules()
        logger.info(f"Rule engine initialized with {len(self.rules)} rules")
    
    def _initialize_rules(self):
        """Initialize clinical decision rules."""
        
        # Cardiac Emergency Rules
        self.rules.append(ClinicalRule(
            rule_id='CARD_001',
            name='Acute Cardiac Event Warning',
            conditions=['chest pain', 'sweating', 'shortness of breath'],
            action='URGENT_CARDIAC_EVALUATION',
            priority='critical',
            category='cardiac',
            explanation='Combination of chest pain, sweating, and breathing difficulty suggests possible cardiac emergency'
        ))
        
        self.rules.append(ClinicalRule(
            rule_id='CARD_002',
            name='Cardiac Risk Indicator',
            conditions=['chest pain', 'palpitations'],
            action='CARDIAC_ASSESSMENT_RECOMMENDED',
            priority='high',
            category='cardiac',
            explanation='Chest pain with palpitations requires cardiac evaluation'
        ))
        
        # Respiratory Emergency Rules
        self.rules.append(ClinicalRule(
            rule_id='RESP_001',
            name='Severe Respiratory Distress',
            conditions=['breathing difficulty', 'chest tightness'],
            action='RESPIRATORY_EMERGENCY',
            priority='critical',
            category='respiratory',
            explanation='Severe breathing difficulty with chest tightness requires immediate attention'
        ))
        
        self.rules.append(ClinicalRule(
            rule_id='RESP_002',
            name='Respiratory Infection Alert',
            conditions=['fever', 'cough', 'breathing difficulty'],
            action='RESPIRATORY_INFECTION_SUSPECTED',
            priority='high',
            category='respiratory',
            explanation='Fever with cough and breathing difficulty suggests respiratory infection'
        ))
        
        # Infection Risk Rules
        self.rules.append(ClinicalRule(
            rule_id='INF_001',
            name='Prolonged Fever Alert',
            conditions=['fever'],  # Duration checked separately
            action='PROLONGED_FEVER_INVESTIGATION',
            priority='medium',
            category='infection',
            explanation='Fever lasting more than 7 days requires investigation'
        ))
        
        self.rules.append(ClinicalRule(
            rule_id='INF_002',
            name='Sepsis Risk Indicator',
            conditions=['fever', 'chills', 'fatigue'],
            action='SEPSIS_RISK_ASSESSMENT',
            priority='high',
            category='infection',
            explanation='Fever with chills and fatigue may indicate systemic infection'
        ))
        
        # Neurological Rules
        self.rules.append(ClinicalRule(
            rule_id='NEURO_001',
            name='Stroke Warning Signs',
            conditions=['headache', 'dizziness', 'weakness'],
            action='NEUROLOGICAL_EMERGENCY',
            priority='critical',
            category='neurological',
            explanation='Combination suggests possible neurological emergency'
        ))
        
        self.rules.append(ClinicalRule(
            rule_id='NEURO_002',
            name='Severe Headache Alert',
            conditions=['headache', 'nausea', 'vomiting'],
            action='SEVERE_HEADACHE_EVALUATION',
            priority='high',
            category='neurological',
            explanation='Severe headache with nausea and vomiting requires evaluation'
        ))
        
        # Gastrointestinal Rules
        self.rules.append(ClinicalRule(
            rule_id='GI_001',
            name='Acute Abdomen Warning',
            conditions=['abdominal pain', 'vomiting', 'fever'],
            action='ACUTE_ABDOMEN_ASSESSMENT',
            priority='high',
            category='gastrointestinal',
            explanation='Acute abdominal pain with vomiting and fever requires urgent assessment'
        ))
        
        self.rules.append(ClinicalRule(
            rule_id='GI_002',
            name='Dehydration Risk',
            conditions=['diarrhea', 'vomiting'],
            action='DEHYDRATION_RISK',
            priority='medium',
            category='gastrointestinal',
            explanation='Diarrhea with vomiting increases dehydration risk'
        ))
        
        # Pain Management Rules
        self.rules.append(ClinicalRule(
            rule_id='PAIN_001',
            name='Severe Pain Alert',
            conditions=['severe pain'],
            action='PAIN_MANAGEMENT_REQUIRED',
            priority='high',
            category='pain',
            explanation='Severe pain requires immediate attention and management'
        ))
    
    def evaluate_symptoms(self, symptoms: List[str], 
                         duration_days: int = None,
                         age: int = None) -> List[Dict]:
        """
        Evaluate symptoms against clinical rules.
        
        Args:
            symptoms: List of patient symptoms
            duration_days: Duration of symptoms in days
            age: Patient age
            
        Returns:
            List of triggered rule flags
        """
        symptoms_set = {s.lower().strip() for s in symptoms}
        triggered_rules = []
        
        for rule in self.rules:
            if rule.evaluate(symptoms_set):
                # Additional checks for specific rules
                if rule.rule_id == 'INF_001' and duration_days:
                    if duration_days < 7:
                        continue  # Skip if fever duration < 7 days
                
                triggered_rules.append(rule.to_dict())
                logger.info(f"Rule triggered: {rule.rule_id} - {rule.name}")
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        triggered_rules.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return triggered_rules
    
    def get_risk_level(self, triggered_rules: List[Dict]) -> str:
        """
        Determine overall risk level based on triggered rules.
        
        Args:
            triggered_rules: List of triggered rules
            
        Returns:
            Risk level: low, medium, high, critical
        """
        if not triggered_rules:
            return 'low'
        
        priorities = [rule['priority'] for rule in triggered_rules]
        
        if 'critical' in priorities:
            return 'critical'
        elif 'high' in priorities:
            return 'high'
        elif 'medium' in priorities:
            return 'medium'
        else:
            return 'low'
    
    def generate_recommendation(self, triggered_rules: List[Dict],
                               risk_level: str) -> str:
        """
        Generate clinical recommendation based on rules.
        
        Args:
            triggered_rules: List of triggered rules
            risk_level: Overall risk level
            
        Returns:
            Clinical recommendation text
        """
        if risk_level == 'critical':
            return ("URGENT: Seek immediate emergency medical attention. "
                   "Call emergency services or go to the nearest emergency room.")
        
        elif risk_level == 'high':
            return ("Seek medical attention promptly. "
                   "Contact your healthcare provider or visit an urgent care facility today.")
        
        elif risk_level == 'medium':
            return ("Schedule an appointment with your healthcare provider within 24-48 hours. "
                   "Monitor symptoms and seek immediate care if they worsen.")
        
        else:
            return ("Monitor symptoms. If symptoms persist or worsen, consult your healthcare provider. "
                   "Maintain hydration and rest.")
    
    def get_all_rules(self) -> List[Dict]:
        """Get all rules as dictionaries."""
        return [rule.to_dict() for rule in self.rules]
    
    def get_rules_by_category(self, category: str) -> List[Dict]:
        """Get rules by category."""
        return [rule.to_dict() for rule in self.rules if rule.category == category]


# Global singleton instance
rule_engine = RuleEngineService()
