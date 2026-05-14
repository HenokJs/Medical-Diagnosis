"""
Model Utilities Module
======================
Utility functions for ML model training, evaluation, and management.

Author: Senior Machine Learning Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from typing import Dict, List, Tuple, Any, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class ModelConfig:
    """Configuration for ML models."""
    
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    
    # Model hyperparameters
    RANDOM_FOREST = {
        'n_estimators': 200,
        'max_depth': 20,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'class_weight': 'balanced',
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    }
    
    DECISION_TREE = {
        'max_depth': 15,
        'min_samples_split': 10,
        'min_samples_leaf': 4,
        'class_weight': 'balanced',
        'random_state': RANDOM_STATE
    }
    
    NAIVE_BAYES = {
        'var_smoothing': 1e-9
    }
    
    LOGISTIC_REGRESSION = {
        'solver': 'lbfgs',
        'max_iter': 5000,
        'class_weight': 'balanced',
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    }
    
    XGBOOST = {
        'n_estimators': 200,
        'max_depth': 10,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    }


class DataLoader:
    """Handles dataset loading and validation."""
    
    def __init__(self, ml_dataset_path: str = 'datasets/ml_dataset.csv'):
        self.ml_dataset_path = ml_dataset_path
        self.df = None
        self.X = None
        self.y = None
        self.feature_columns = None
        
    def load_dataset(self) -> pd.DataFrame:
        """Load and validate ML dataset."""
        print("\n" + "="*70)
        print("STEP 1: LOADING DATASET")
        print("="*70)
        
        # Load dataset
        print(f"\nLoading dataset from: {self.ml_dataset_path}")
        self.df = pd.read_csv(self.ml_dataset_path)
        
        # Verify integrity
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {self.df.shape}")
        print(f"  Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Validate structure
        if 'disease' not in self.df.columns:
            raise ValueError("Dataset missing 'disease' column")
        
        # Get feature columns
        self.feature_columns = [col for col in self.df.columns if col != 'disease']
        
        # Print statistics
        self._print_statistics()
        
        return self.df
    
    def _print_statistics(self):
        """Print comprehensive dataset statistics."""
        print("\n" + "-"*70)
        print("DATASET STATISTICS")
        print("-"*70)
        
        # Basic stats
        print(f"\nTotal samples: {len(self.df):,}")
        print(f"Total features: {len(self.feature_columns)}")
        print(f"Total diseases: {self.df['disease'].nunique()}")
        
        # Disease distribution
        print("\nDisease Distribution:")
        disease_counts = self.df['disease'].value_counts()
        print(f"  Min samples per disease: {disease_counts.min()}")
        print(f"  Max samples per disease: {disease_counts.max()}")
        print(f"  Mean samples per disease: {disease_counts.mean():.1f}")
        print(f"  Median samples per disease: {disease_counts.median():.1f}")
        
        # Class balance
        balance_ratio = disease_counts.min() / disease_counts.max()
        print(f"\nClass Balance Ratio: {balance_ratio:.3f}")
        if balance_ratio < 0.5:
            print("  ⚠ Warning: Significant class imbalance detected")
        else:
            print("  ✓ Classes are reasonably balanced")
        
        # Feature sparsity
        feature_data = self.df[self.feature_columns]
        sparsity = (feature_data == 0).sum().sum() / (feature_data.shape[0] * feature_data.shape[1])
        print(f"\nFeature Sparsity: {sparsity:.2%}")
        print(f"  Non-zero values: {(1-sparsity):.2%}")
        
        # Data quality
        null_count = self.df.isnull().sum().sum()
        print(f"\nData Quality:")
        print(f"  Null values: {null_count}")
        print(f"  Duplicate rows: {self.df.duplicated().sum()}")
        
        # Feature statistics
        print(f"\nFeature Statistics:")
        print(f"  Features with all zeros: {(feature_data.sum() == 0).sum()}")
        print(f"  Features with all ones: {(feature_data.sum() == len(feature_data)).sum()}")
        
        # Top diseases
        print("\nTop 10 Diseases by Sample Count:")
        for idx, (disease, count) in enumerate(disease_counts.head(10).items(), 1):
            print(f"  {idx:2d}. {disease:30s} {count:5d} samples")
    
    def prepare_data(self) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        """Prepare features and labels."""
        print("\n" + "="*70)
        print("STEP 2: DATA PREPARATION")
        print("="*70)
        
        # Separate features and labels
        self.X = self.df[self.feature_columns]
        self.y = self.df['disease']
        
        print(f"\n✓ Features (X): {self.X.shape}")
        print(f"✓ Labels (y): {self.y.shape}")
        print(f"✓ Feature columns: {len(self.feature_columns)}")
        
        return self.X, self.y, self.feature_columns


class ModelEvaluator:
    """Handles model evaluation and metrics calculation."""
    
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, 
                         y_proba: Optional[np.ndarray] = None,
                         label_encoder: Any = None) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Prediction probabilities (optional)
            label_encoder: Label encoder for class names
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
        
        # Calculate top-3 accuracy if probabilities available
        if y_proba is not None:
            metrics['top3_accuracy'] = ModelEvaluator.calculate_top_k_accuracy(
                y_true, y_proba, k=3, label_encoder=label_encoder
            )
        
        return metrics
    
    @staticmethod
    def calculate_top_k_accuracy(y_true: np.ndarray, y_proba: np.ndarray, 
                                 k: int = 3, label_encoder: Any = None) -> float:
        """
        Calculate top-k accuracy (clinically critical metric).
        
        Args:
            y_true: True labels (already encoded as integers)
            y_proba: Prediction probabilities
            k: Number of top predictions to consider
            label_encoder: Label encoder (not used, kept for compatibility)
            
        Returns:
            Top-k accuracy score
        """
        # y_true is already encoded as integers
        y_true_encoded = y_true
        
        # Get top k predictions
        top_k_preds = np.argsort(y_proba, axis=1)[:, -k:]
        
        # Check if true label is in top k
        correct = 0
        for i, true_label in enumerate(y_true_encoded):
            if true_label in top_k_preds[i]:
                correct += 1
        
        return correct / len(y_true)
    
    @staticmethod
    def generate_classification_report(y_true: np.ndarray, y_pred: np.ndarray,
                                      target_names: List[str]) -> str:
        """Generate detailed classification report."""
        return classification_report(y_true, y_pred, target_names=target_names, 
                                    zero_division=0)
    
    @staticmethod
    def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray,
                             labels: List[str], save_path: str,
                             title: str = "Confusion Matrix"):
        """
        Plot and save confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            labels: Class labels
            save_path: Path to save figure
            title: Plot title
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(16, 14))
        
        # Use percentage for better readability
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Plot with annotations
        sns.heatmap(cm_percent, annot=False, fmt='.1f', cmap='Blues',
                   xticklabels=labels, yticklabels=labels,
                   cbar_kws={'label': 'Percentage (%)'})
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.ylabel('True Disease', fontsize=12)
        plt.xlabel('Predicted Disease', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Confusion matrix saved to: {save_path}")


class ModelSaver:
    """Handles model and artifact saving."""
    
    def __init__(self, save_dir: str = 'models/saved'):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def save_model(self, model: Any, model_name: str) -> str:
        """
        Save trained model.
        
        Args:
            model: Trained model object
            model_name: Name for the model file
            
        Returns:
            Path to saved model
        """
        filepath = os.path.join(self.save_dir, f"{model_name}.pkl")
        joblib.dump(model, filepath)
        print(f"✓ Model saved: {filepath}")
        return filepath
    
    def save_encoder(self, encoder: Any, name: str = 'label_encoder') -> str:
        """Save label encoder."""
        filepath = os.path.join(self.save_dir, f"{name}.pkl")
        joblib.dump(encoder, filepath)
        print(f"✓ Encoder saved: {filepath}")
        return filepath
    
    def save_feature_columns(self, columns: List[str], 
                            name: str = 'feature_columns') -> str:
        """Save feature column names."""
        filepath = os.path.join(self.save_dir, f"{name}.pkl")
        joblib.dump(columns, filepath)
        print(f"✓ Feature columns saved: {filepath}")
        return filepath
    
    def save_metadata(self, metadata: Dict, name: str = 'model_metadata') -> str:
        """Save model metadata."""
        filepath = os.path.join(self.save_dir, f"{name}.json")
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata saved: {filepath}")
        return filepath
    
    def load_model(self, model_name: str) -> Any:
        """Load saved model."""
        filepath = os.path.join(self.save_dir, f"{model_name}.pkl")
        return joblib.load(filepath)
    
    def load_encoder(self, name: str = 'label_encoder') -> Any:
        """Load label encoder."""
        filepath = os.path.join(self.save_dir, f"{name}.pkl")
        return joblib.load(filepath)
    
    def load_feature_columns(self, name: str = 'feature_columns') -> List[str]:
        """Load feature columns."""
        filepath = os.path.join(self.save_dir, f"{name}.pkl")
        return joblib.load(filepath)


class ReportGenerator:
    """Generates training reports and visualizations."""
    
    def __init__(self, report_dir: str = 'reports/model_training'):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def save_comparison_table(self, results: List[Dict], 
                              filename: str = 'model_comparison.csv'):
        """Save model comparison table."""
        df = pd.DataFrame(results)
        filepath = os.path.join(self.report_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"✓ Comparison table saved: {filepath}")
        return filepath
    
    def plot_accuracy_comparison(self, results: List[Dict],
                                 filename: str = 'accuracy_chart.png'):
        """Plot accuracy comparison chart."""
        df = pd.DataFrame(results)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Regular accuracy
        ax1.bar(df['model'], df['accuracy'], color='steelblue', alpha=0.8)
        ax1.set_xlabel('Model', fontsize=12)
        ax1.set_ylabel('Accuracy', fontsize=12)
        ax1.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylim([0, 1])
        ax1.tick_params(axis='x', rotation=45)
        for i, v in enumerate(df['accuracy']):
            ax1.text(i, v + 0.02, f'{v:.4f}', ha='center', fontsize=10)
        
        # Top-3 accuracy
        if 'top3_accuracy' in df.columns:
            ax2.bar(df['model'], df['top3_accuracy'], color='coral', alpha=0.8)
            ax2.set_xlabel('Model', fontsize=12)
            ax2.set_ylabel('Top-3 Accuracy', fontsize=12)
            ax2.set_title('Model Top-3 Accuracy Comparison', fontsize=14, fontweight='bold')
            ax2.set_ylim([0, 1])
            ax2.tick_params(axis='x', rotation=45)
            for i, v in enumerate(df['top3_accuracy']):
                ax2.text(i, v + 0.02, f'{v:.4f}', ha='center', fontsize=10)
        
        plt.tight_layout()
        filepath = os.path.join(self.report_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Accuracy chart saved: {filepath}")
    
    def plot_feature_importance(self, feature_importance: pd.DataFrame,
                               top_n: int = 20,
                               filename: str = 'feature_importance.png'):
        """Plot feature importance."""
        top_features = feature_importance.head(top_n)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(top_features)), top_features['importance'], color='teal')
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Symptom', fontsize=12)
        plt.title(f'Top {top_n} Most Important Symptoms', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(top_features['importance']):
            plt.text(v + 0.001, i, f'{v:.4f}', va='center', fontsize=9)
        
        plt.tight_layout()
        filepath = os.path.join(self.report_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Feature importance chart saved: {filepath}")


def format_time(seconds: float) -> str:
    """Format time in human-readable format."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def print_section_header(title: str):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)


def print_subsection_header(title: str):
    """Print formatted subsection header."""
    print("\n" + "-"*70)
    print(f" {title}")
    print("-"*70)
