"""
Inference Engine
================
Production-ready inference engine for medical diagnosis predictions.

Author: Senior Machine Learning Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import joblib
import json
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')


class DiagnosisInferenceEngine:
    """
    Production inference engine for medical diagnosis.
    
    Features:
    - Top-3 disease predictions
    - Confidence scores
    - Severity information
    - Explainability
    """
    
    def __init__(self, model_dir: str = 'models/saved'):
        """
        Initialize inference engine.
        
        Args:
            model_dir: Directory containing saved models
        """
        self.model_dir = model_dir
        self.model = None
        self.label_encoder = None
        self.feature_columns = None
        self.master_data = None
        self.metadata = None
        
        self._load_artifacts()
    
    def _load_artifacts(self):
        """Load all required artifacts."""
        print("Loading inference artifacts...")
        
        # Load best model
        model_path = f'{self.model_dir}/best_model.pkl'
        self.model = joblib.load(model_path)
        print(f"✓ Model loaded: {model_path}")
        
        # Load label encoder
        encoder_path = f'{self.model_dir}/label_encoder.pkl'
        self.label_encoder = joblib.load(encoder_path)
        print(f"✓ Label encoder loaded: {encoder_path}")
        
        # Load feature columns
        features_path = f'{self.model_dir}/feature_columns.pkl'
        self.feature_columns = joblib.load(features_path)
        print(f"✓ Feature columns loaded: {features_path}")
        
        # Load metadata
        try:
            metadata_path = f'{self.model_dir}/model_metadata.json'
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print(f"✓ Metadata loaded: {metadata_path}")
        except:
            print("⚠ Metadata not found (optional)")
        
        # Load master dataset for severity info
        try:
            self.master_data = pd.read_csv('datasets/master_dataset.csv')
            print(f"✓ Master dataset loaded for severity info")
        except:
            print("⚠ Master dataset not found (severity info unavailable)")
        
        print(f"\n✓ Inference engine ready")
        print(f"  Model: {self.metadata.get('best_model', 'Unknown') if self.metadata else 'Unknown'}")
        print(f"  Features: {len(self.feature_columns)}")
        print(f"  Diseases: {len(self.label_encoder.classes_)}")
    
    def _prepare_input(self, symptoms: List[str]) -> np.ndarray:
        """
        Prepare symptom input for model.
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            Feature vector
        """
        # Create feature vector (all zeros)
        feature_vector = np.zeros(len(self.feature_columns))
        
        # Set symptoms to 1
        for symptom in symptoms:
            # Normalize symptom name
            symptom_normalized = symptom.lower().strip()
            
            # Find matching feature
            if symptom_normalized in self.feature_columns:
                idx = self.feature_columns.index(symptom_normalized)
                feature_vector[idx] = 1
        
        return feature_vector.reshape(1, -1)
    
    def _get_severity(self, disease: str) -> str:
        """
        Get severity level for a disease.
        
        Args:
            disease: Disease name
            
        Returns:
            Severity level
        """
        if self.master_data is None:
            return "unknown"
        
        disease_row = self.master_data[self.master_data['disease'] == disease]
        if len(disease_row) > 0:
            return disease_row.iloc[0]['severity']
        
        return "unknown"
    
    def _get_disease_info(self, disease: str) -> Dict:
        """
        Get comprehensive disease information.
        
        Args:
            disease: Disease name
            
        Returns:
            Disease information dictionary
        """
        info = {
            'disease': disease,
            'severity': self._get_severity(disease),
            'description': '',
            'precautions': []
        }
        
        if self.master_data is not None:
            disease_row = self.master_data[self.master_data['disease'] == disease]
            if len(disease_row) > 0:
                row = disease_row.iloc[0]
                info['description'] = row.get('description', '')
                
                precautions = row.get('precautions', '')
                if isinstance(precautions, str) and precautions:
                    info['precautions'] = precautions.split('|')
        
        return info
    
    def predict_disease(self, symptoms: List[str], top_k: int = 3,
                       include_details: bool = True) -> Dict:
        """
        Predict disease from symptoms.
        
        Args:
            symptoms: List of symptom names
            top_k: Number of top predictions to return
            include_details: Include disease details and explainability
            
        Returns:
            Prediction results dictionary
        """
        # Validate input
        if not symptoms or len(symptoms) == 0:
            return {
                'error': 'No symptoms provided',
                'top_predictions': []
            }
        
        # Prepare input
        X = self._prepare_input(symptoms)
        
        # Get predictions
        probabilities = self.model.predict_proba(X)[0]
        
        # Get top-k predictions
        top_k_indices = np.argsort(probabilities)[-top_k:][::-1]
        
        # Build results
        predictions = []
        for idx in top_k_indices:
            disease = self.label_encoder.classes_[idx]
            confidence = float(probabilities[idx])
            
            prediction = {
                'disease': disease,
                'confidence': confidence,
                'confidence_percent': f"{confidence * 100:.2f}%"
            }
            
            # Add details if requested
            if include_details:
                disease_info = self._get_disease_info(disease)
                prediction.update({
                    'severity': disease_info['severity'],
                    'description': disease_info['description'],
                    'precautions': disease_info['precautions']
                })
            
            predictions.append(prediction)
        
        # Build response
        result = {
            'input_symptoms': symptoms,
            'matched_symptoms': self._get_matched_symptoms(symptoms),
            'top_predictions': predictions,
            'prediction_count': len(predictions)
        }
        
        # Add explainability if available
        if include_details and hasattr(self.model, 'feature_importances_'):
            result['explainability'] = self._explain_prediction(X, predictions[0]['disease'])
        
        return result
    
    def _get_matched_symptoms(self, symptoms: List[str]) -> List[str]:
        """
        Get list of symptoms that matched features.
        
        Args:
            symptoms: Input symptoms
            
        Returns:
            List of matched symptoms
        """
        matched = []
        for symptom in symptoms:
            symptom_normalized = symptom.lower().strip()
            if symptom_normalized in self.feature_columns:
                matched.append(symptom_normalized)
        
        return matched
    
    def _explain_prediction(self, X: np.ndarray, disease: str) -> Dict:
        """
        Generate explainability for prediction.
        
        Args:
            X: Feature vector
            disease: Predicted disease
            
        Returns:
            Explainability dictionary
        """
        if not hasattr(self.model, 'feature_importances_'):
            return {}
        
        # Get feature importances
        importances = self.model.feature_importances_
        
        # Get active features (symptoms present)
        active_features = np.where(X[0] == 1)[0]
        
        # Get importance of active features
        active_importances = [(self.feature_columns[i], importances[i]) 
                             for i in active_features]
        active_importances.sort(key=lambda x: x[1], reverse=True)
        
        # Get top overall important features
        top_features_idx = np.argsort(importances)[-10:][::-1]
        top_features = [(self.feature_columns[i], importances[i]) 
                       for i in top_features_idx]
        
        return {
            'disease': disease,
            'active_symptoms': [f[0] for f in active_importances],
            'active_symptom_importance': [
                {'symptom': f[0], 'importance': float(f[1])} 
                for f in active_importances
            ],
            'top_important_features': [
                {'feature': f[0], 'importance': float(f[1])} 
                for f in top_features[:5]
            ]
        }
    
    def explain_prediction(self, symptoms: List[str], disease: str) -> Dict:
        """
        Explain why a specific disease was predicted.
        
        Args:
            symptoms: Input symptoms
            disease: Disease to explain
            
        Returns:
            Explanation dictionary
        """
        X = self._prepare_input(symptoms)
        
        explanation = {
            'disease': disease,
            'input_symptoms': symptoms,
            'matched_symptoms': self._get_matched_symptoms(symptoms),
            'severity': self._get_severity(disease)
        }
        
        # Add feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            explain_data = self._explain_prediction(X, disease)
            explanation.update(explain_data)
        
        return explanation
    
    def batch_predict(self, symptom_lists: List[List[str]], 
                     top_k: int = 3) -> List[Dict]:
        """
        Batch prediction for multiple symptom sets.
        
        Args:
            symptom_lists: List of symptom lists
            top_k: Number of top predictions per input
            
        Returns:
            List of prediction results
        """
        results = []
        for symptoms in symptom_lists:
            result = self.predict_disease(symptoms, top_k=top_k, include_details=False)
            results.append(result)
        
        return results
    
    def get_model_info(self) -> Dict:
        """Get model information."""
        info = {
            'model_type': type(self.model).__name__,
            'num_features': len(self.feature_columns),
            'num_diseases': len(self.label_encoder.classes_),
            'diseases': self.label_encoder.classes_.tolist()
        }
        
        if self.metadata:
            info.update({
                'best_model': self.metadata.get('best_model'),
                'accuracy': self.metadata.get('metrics', {}).get('accuracy'),
                'top3_accuracy': self.metadata.get('metrics', {}).get('top3_accuracy'),
                'training_date': self.metadata.get('training_date')
            })
        
        return info


def demo_inference():
    """Demonstration of inference engine."""
    print("\n" + "="*70)
    print(" INFERENCE ENGINE DEMONSTRATION")
    print("="*70)
    
    # Initialize engine
    engine = DiagnosisInferenceEngine()
    
    # Example 1: Simple prediction
    print("\n" + "-"*70)
    print("Example 1: Respiratory Symptoms")
    print("-"*70)
    
    symptoms1 = ['fever', 'cough', 'fatigue', 'headache']
    result1 = engine.predict_disease(symptoms1, top_k=3)
    
    print(f"\nInput Symptoms: {symptoms1}")
    print(f"Matched Symptoms: {result1['matched_symptoms']}")
    print(f"\nTop 3 Predictions:")
    for i, pred in enumerate(result1['top_predictions'], 1):
        print(f"\n{i}. {pred['disease']}")
        print(f"   Confidence: {pred['confidence_percent']}")
        print(f"   Severity: {pred['severity']}")
        if pred['precautions']:
            print(f"   Precautions: {', '.join(pred['precautions'][:2])}")
    
    # Example 2: Different symptoms
    print("\n" + "-"*70)
    print("Example 2: Gastrointestinal Symptoms")
    print("-"*70)
    
    symptoms2 = ['nausea', 'vomiting', 'abdominal pain', 'diarrhea']
    result2 = engine.predict_disease(symptoms2, top_k=3, include_details=False)
    
    print(f"\nInput Symptoms: {symptoms2}")
    print(f"\nTop 3 Predictions:")
    for i, pred in enumerate(result2['top_predictions'], 1):
        print(f"{i}. {pred['disease']:30s} {pred['confidence_percent']}")
    
    # Example 3: Explainability
    print("\n" + "-"*70)
    print("Example 3: Prediction Explainability")
    print("-"*70)
    
    if result1['top_predictions']:
        top_disease = result1['top_predictions'][0]['disease']
        explanation = engine.explain_prediction(symptoms1, top_disease)
        
        print(f"\nExplaining prediction: {top_disease}")
        print(f"Matched symptoms: {explanation['matched_symptoms']}")
        print(f"Severity: {explanation['severity']}")
    
    # Model info
    print("\n" + "-"*70)
    print("Model Information")
    print("-"*70)
    
    info = engine.get_model_info()
    print(f"\nModel Type: {info['model_type']}")
    print(f"Features: {info['num_features']}")
    print(f"Diseases: {info['num_diseases']}")
    if 'accuracy' in info:
        print(f"Accuracy: {info['accuracy']:.4f}")
    if 'top3_accuracy' in info:
        print(f"Top-3 Accuracy: {info['top3_accuracy']:.4f}")
    
    print("\n" + "="*70)
    print(" ✓ INFERENCE ENGINE READY FOR PRODUCTION")
    print("="*70)


if __name__ == "__main__":
    demo_inference()
