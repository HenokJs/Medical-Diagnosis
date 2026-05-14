"""
ML Service Layer
================
Machine Learning inference service with singleton pattern.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class MLService:
    """
    Singleton ML inference service.
    
    Responsibilities:
    - Load trained models once
    - Provide fast inference
    - Manage feature encoding
    - Return ranked predictions
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize ML service (only once)."""
        if not MLService._initialized:
            self.model = None
            self.label_encoder = None
            self.feature_columns = None
            self.metadata = None
            self.master_data = None
            
            MLService._initialized = True
            logger.info("MLService instance created")
    
    def load_models(self, model_dir: str, dataset_dir: str):
        """
        Load all ML artifacts.
        
        Args:
            model_dir: Directory containing saved models
            dataset_dir: Directory containing datasets
        """
        try:
            logger.info("Loading ML models...")
            
            # Load best model
            model_path = os.path.join(model_dir, 'best_model.pkl')
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded: {model_path}")
            
            # Load label encoder
            encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
            self.label_encoder = joblib.load(encoder_path)
            logger.info(f"Label encoder loaded: {encoder_path}")
            
            # Load feature columns
            features_path = os.path.join(model_dir, 'feature_columns.pkl')
            self.feature_columns = joblib.load(features_path)
            logger.info(f"Feature columns loaded: {features_path}")
            
            # Load metadata
            try:
                import json
                metadata_path = os.path.join(model_dir, 'model_metadata.json')
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"Metadata loaded: {metadata_path}")
            except Exception as e:
                logger.warning(f"Metadata not loaded: {e}")
                self.metadata = {}
            
            # Load master dataset for disease info
            try:
                master_path = os.path.join(dataset_dir, 'master_dataset.csv')
                self.master_data = pd.read_csv(master_path)
                logger.info(f"Master dataset loaded: {master_path}")
            except Exception as e:
                logger.warning(f"Master dataset not loaded: {e}")
                self.master_data = None
            
            logger.info("All ML artifacts loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")
            raise RuntimeError(f"ML model loading failed: {e}")
    
    def is_loaded(self) -> bool:
        """Check if models are loaded."""
        return (self.model is not None and 
                self.label_encoder is not None and 
                self.feature_columns is not None)
    
    def _prepare_features(self, symptoms: List[str]) -> np.ndarray:
        """
        Prepare feature vector from symptoms.
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            Feature vector
        """
        # Create zero vector
        feature_vector = np.zeros(len(self.feature_columns))
        
        # Set symptoms to 1
        for symptom in symptoms:
            symptom_normalized = symptom.lower().strip()
            if symptom_normalized in self.feature_columns:
                idx = self.feature_columns.index(symptom_normalized)
                feature_vector[idx] = 1
        
        return feature_vector.reshape(1, -1)
    
    def _get_disease_info(self, disease: str) -> Dict:
        """
        Get disease information from master dataset.
        
        Args:
            disease: Disease name
            
        Returns:
            Disease information dictionary
        """
        info = {
            'disease': disease,
            'severity': 'unknown',
            'description': '',
            'precautions': []
        }
        
        if self.master_data is not None:
            disease_row = self.master_data[self.master_data['disease'] == disease]
            if len(disease_row) > 0:
                row = disease_row.iloc[0]
                info['severity'] = row.get('severity', 'unknown')
                info['description'] = row.get('description', '')
                
                precautions = row.get('precautions', '')
                if isinstance(precautions, str) and precautions:
                    info['precautions'] = precautions.split('|')
        
        return info
    
    def predict(self, symptoms: List[str], top_k: int = 3) -> List[Dict]:
        """
        Predict diseases from symptoms.
        
        Args:
            symptoms: List of symptom names
            top_k: Number of top predictions
            
        Returns:
            List of predictions with confidence scores
        """
        if not self.is_loaded():
            raise RuntimeError("ML models not loaded")
        
        if not symptoms:
            raise ValueError("No symptoms provided")
        
        # Prepare features
        X = self._prepare_features(symptoms)
        
        # Get predictions
        probabilities = self.model.predict_proba(X)[0]
        
        # Get top-k predictions
        top_k_indices = np.argsort(probabilities)[-top_k:][::-1]
        
        # Build predictions
        predictions = []
        for idx in top_k_indices:
            disease = self.label_encoder.classes_[idx]
            confidence = float(probabilities[idx])
            
            # Get disease info
            disease_info = self._get_disease_info(disease)
            
            prediction = {
                'disease': disease,
                'confidence': confidence,
                'confidence_percent': f"{confidence * 100:.2f}%",
                'severity': disease_info['severity'],
                'description': disease_info['description'],
                'precautions': disease_info['precautions']
            }
            
            predictions.append(prediction)
        
        return predictions
    
    def get_matched_symptoms(self, symptoms: List[str]) -> List[str]:
        """
        Get symptoms that matched features.
        
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
    
    def get_feature_importance(self, symptoms: List[str], top_n: int = 5) -> List[Dict]:
        """
        Get feature importance for active symptoms.
        
        Args:
            symptoms: Input symptoms
            top_n: Number of top features
            
        Returns:
            List of important features
        """
        if not hasattr(self.model, 'feature_importances_'):
            return []
        
        # Get feature importances
        importances = self.model.feature_importances_
        
        # Get active features
        X = self._prepare_features(symptoms)
        active_features = np.where(X[0] == 1)[0]
        
        # Get importance of active features
        active_importances = [(self.feature_columns[i], importances[i]) 
                             for i in active_features]
        active_importances.sort(key=lambda x: x[1], reverse=True)
        
        # Format results
        results = [
            {'symptom': symptom, 'importance': float(importance)}
            for symptom, importance in active_importances[:top_n]
        ]
        
        return results
    
    def get_model_info(self) -> Dict:
        """Get model information."""
        info = {
            'model_type': type(self.model).__name__ if self.model else 'Not loaded',
            'num_features': len(self.feature_columns) if self.feature_columns else 0,
            'num_diseases': len(self.label_encoder.classes_) if self.label_encoder else 0,
            'loaded': self.is_loaded()
        }
        
        if self.metadata:
            info.update({
                'best_model': self.metadata.get('best_model'),
                'accuracy': self.metadata.get('metrics', {}).get('accuracy'),
                'top3_accuracy': self.metadata.get('metrics', {}).get('top3_accuracy'),
                'training_date': self.metadata.get('training_date')
            })
        
        return info
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all diseases."""
        if self.label_encoder:
            return self.label_encoder.classes_.tolist()
        return []
    
    def get_all_symptoms(self) -> List[str]:
        """Get list of all symptoms."""
        if self.feature_columns:
            return self.feature_columns
        return []


# Global singleton instance
ml_service = MLService()
