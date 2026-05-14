"""
Model Evaluation Module
========================
Comprehensive model evaluation and analysis.

Author: Senior Machine Learning Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import joblib
from typing import Dict, List
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from model_utils import ModelEvaluator, print_section_header


class ModelAnalyzer:
    """Comprehensive model analysis and evaluation."""
    
    def __init__(self, model_dir: str = 'models/saved'):
        self.model_dir = model_dir
        self.evaluator = ModelEvaluator()
        
        # Load artifacts
        self.model = joblib.load(f'{model_dir}/best_model.pkl')
        self.label_encoder = joblib.load(f'{model_dir}/label_encoder.pkl')
        self.feature_columns = joblib.load(f'{model_dir}/feature_columns.pkl')
        
        # Load test data
        self._load_test_data()
    
    def _load_test_data(self):
        """Load and prepare test data."""
        from sklearn.model_selection import train_test_split
        from model_utils import ModelConfig
        
        # Load dataset
        df = pd.read_csv('datasets/ml_dataset.csv')
        
        # Prepare data
        X = df[[col for col in df.columns if col != 'disease']]
        y = df['disease']
        
        # Encode labels
        y_encoded = self.label_encoder.transform(y)
        
        # Split (same as training)
        _, self.X_test, _, self.y_test = train_test_split(
            X, y_encoded,
            test_size=ModelConfig.TEST_SIZE,
            random_state=ModelConfig.RANDOM_STATE,
            stratify=y_encoded
        )
    
    def generate_detailed_report(self):
        """Generate detailed classification report."""
        print_section_header("DETAILED CLASSIFICATION REPORT")
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        y_proba = self.model.predict_proba(self.X_test)
        
        # Classification report
        report = classification_report(
            self.y_test, y_pred,
            target_names=self.label_encoder.classes_,
            digits=4
        )
        
        print("\nPer-Disease Performance:")
        print(report)
        
        # Save report
        report_path = 'reports/model_training/classification_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Detailed Classification Report\n\n")
            f.write("## Per-Disease Performance\n\n")
            f.write("```\n")
            f.write(report)
            f.write("\n```\n")
        
        print(f"\n✓ Report saved: {report_path}")
        
        return report
    
    def analyze_top3_performance(self):
        """Analyze top-3 prediction performance."""
        print_section_header("TOP-3 ACCURACY ANALYSIS")
        
        y_proba = self.model.predict_proba(self.X_test)
        
        # Calculate top-k accuracies
        accuracies = {}
        for k in [1, 2, 3, 5]:
            acc = self.evaluator.calculate_top_k_accuracy(
                self.y_test, y_proba, k=k
            )
            accuracies[f'top{k}'] = acc
            print(f"Top-{k} Accuracy: {acc:.4f} ({acc*100:.2f}%)")
        
        # Generate report
        report = f"""# Top-K Accuracy Analysis

## Clinical Significance

Top-K accuracy measures how often the correct diagnosis appears in the top K predictions. This is **clinically critical** because:

1. **Differential Diagnosis:** Physicians consider multiple possibilities
2. **Risk Mitigation:** Reduces chance of missing correct diagnosis
3. **Decision Support:** Provides ranked alternatives
4. **Real-World Alignment:** Matches clinical practice patterns

## Results

| Metric | Accuracy | Percentage |
|--------|----------|------------|
| Top-1 (Standard) | {accuracies['top1']:.4f} | {accuracies['top1']*100:.2f}% |
| Top-2 | {accuracies['top2']:.4f} | {accuracies['top2']*100:.2f}% |
| Top-3 | {accuracies['top3']:.4f} | {accuracies['top3']*100:.2f}% |
| Top-5 | {accuracies['top5']:.4f} | {accuracies['top5']*100:.2f}% |

## Interpretation

- **Top-1 Accuracy ({accuracies['top1']*100:.2f}%):** Model's primary prediction is correct
- **Top-3 Accuracy ({accuracies['top3']*100:.2f}%):** Correct diagnosis in top 3 predictions
- **Improvement:** {(accuracies['top3'] - accuracies['top1'])*100:.2f}% gain from considering top 3

## Clinical Application

In a clinical setting:
- Present top 3 predictions to physician
- Include confidence scores
- Provide symptom-disease relationships
- Support, not replace, clinical judgment

## Recommendation

✓ **Use Top-3 predictions in production**  
✓ **Display all 3 with confidence scores**  
✓ **Include severity and precautions**  
✓ **Enable physician override**
"""
        
        # Save report
        report_path = 'reports/model_training/top3_accuracy_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✓ Top-3 report saved: {report_path}")
        
        return accuracies
    
    def analyze_errors(self):
        """Analyze prediction errors."""
        print_section_header("ERROR ANALYSIS")
        
        y_pred = self.model.predict(self.X_test)
        
        # Find errors
        errors = self.y_test != y_pred
        error_indices = np.where(errors)[0]
        
        print(f"\nTotal Errors: {errors.sum()} / {len(self.y_test)}")
        print(f"Error Rate: {errors.sum() / len(self.y_test):.4f}")
        
        # Analyze error patterns
        if errors.sum() > 0:
            print("\nError Distribution by True Disease:")
            error_diseases = self.label_encoder.inverse_transform(self.y_test[errors])
            error_counts = pd.Series(error_diseases).value_counts()
            
            print(error_counts.head(10))
    
    def run_complete_evaluation(self):
        """Run complete evaluation."""
        print("\n" + "="*70)
        print(" COMPREHENSIVE MODEL EVALUATION")
        print("="*70)
        
        # Detailed report
        self.generate_detailed_report()
        
        # Top-3 analysis
        self.analyze_top3_performance()
        
        # Error analysis
        self.analyze_errors()
        
        print("\n" + "="*70)
        print(" ✓ EVALUATION COMPLETE")
        print("="*70)


def main():
    """Main evaluation function."""
    analyzer = ModelAnalyzer()
    analyzer.run_complete_evaluation()


if __name__ == "__main__":
    main()
