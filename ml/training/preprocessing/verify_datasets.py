"""
Dataset Verification Script
============================
Validates the generated datasets and provides quality checks.

Author: Senior AI/ML Data Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List

class DatasetVerifier:
    """Verifies the quality and integrity of generated datasets."""
    
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
    
    def check_file_exists(self, filepath: str) -> bool:
        """Check if a file exists."""
        if os.path.exists(filepath):
            self.results['passed'].append(f"✓ File exists: {filepath}")
            return True
        else:
            self.results['failed'].append(f"✗ File missing: {filepath}")
            return False
    
    def verify_master_dataset(self):
        """Verify master dataset."""
        print("\n" + "="*60)
        print("VERIFYING MASTER DATASET")
        print("="*60)
        
        filepath = 'datasets/master_dataset.csv'
        if not self.check_file_exists(filepath):
            return
        
        df = pd.read_csv(filepath)
        
        # Check shape
        print(f"\nShape: {df.shape}")
        if df.shape[0] == 50:
            self.results['passed'].append("✓ Master dataset has 50 diseases")
        else:
            self.results['failed'].append(f"✗ Expected 50 diseases, got {df.shape[0]}")
        
        # Check columns
        expected_cols = ['disease', 'symptoms', 'description', 'precautions', 
                        'severity', 'nlp_examples', 'symptom_count']
        if list(df.columns) == expected_cols:
            self.results['passed'].append("✓ All expected columns present")
        else:
            self.results['failed'].append(f"✗ Column mismatch: {df.columns.tolist()}")
        
        # Check for nulls
        null_counts = df.isnull().sum()
        if null_counts.sum() == 0:
            self.results['passed'].append("✓ No null values")
        else:
            self.results['warnings'].append(f"⚠ Null values found: {null_counts[null_counts > 0].to_dict()}")
        
        # Check severity values
        valid_severities = {'minor', 'moderate', 'urgent', 'critical'}
        invalid_severities = set(df['severity'].unique()) - valid_severities
        if len(invalid_severities) == 0:
            self.results['passed'].append("✓ All severity values valid")
        else:
            self.results['failed'].append(f"✗ Invalid severities: {invalid_severities}")
        
        print(f"Diseases: {df['disease'].nunique()}")
        print(f"Severity distribution:\n{df['severity'].value_counts()}")
        print(f"Avg symptoms per disease: {df['symptom_count'].mean():.1f}")
    
    def verify_ml_dataset(self):
        """Verify ML dataset."""
        print("\n" + "="*60)
        print("VERIFYING ML DATASET")
        print("="*60)
        
        filepath = 'datasets/ml_dataset.csv'
        if not self.check_file_exists(filepath):
            return
        
        df = pd.read_csv(filepath)
        
        # Check shape
        print(f"\nShape: {df.shape}")
        if df.shape[0] > 0:
            self.results['passed'].append(f"✓ ML dataset has {df.shape[0]} samples")
        else:
            self.results['failed'].append("✗ ML dataset is empty")
        
        # Check disease column
        if 'disease' in df.columns:
            self.results['passed'].append("✓ Disease column present")
            print(f"Diseases: {df['disease'].nunique()}")
            print(f"Samples per disease: {df['disease'].value_counts().describe()}")
        else:
            self.results['failed'].append("✗ Disease column missing")
        
        # Check feature columns (should be binary)
        feature_cols = [col for col in df.columns if col != 'disease']
        if len(feature_cols) > 0:
            self.results['passed'].append(f"✓ {len(feature_cols)} feature columns")
            
            # Check if features are binary
            non_binary_cols = []
            for col in feature_cols[:10]:  # Check first 10
                unique_vals = df[col].unique()
                if not set(unique_vals).issubset({0, 1, np.nan}):
                    non_binary_cols.append(col)
            
            if len(non_binary_cols) == 0:
                self.results['passed'].append("✓ Features are binary (0/1)")
            else:
                self.results['warnings'].append(f"⚠ Non-binary features: {non_binary_cols}")
        else:
            self.results['failed'].append("✗ No feature columns found")
    
    def verify_nlp_dataset(self):
        """Verify NLP dataset."""
        print("\n" + "="*60)
        print("VERIFYING NLP DATASET")
        print("="*60)
        
        filepath = 'datasets/nlp_dataset.csv'
        if not self.check_file_exists(filepath):
            return
        
        df = pd.read_csv(filepath)
        
        # Check shape
        print(f"\nShape: {df.shape}")
        if df.shape[0] > 0:
            self.results['passed'].append(f"✓ NLP dataset has {df.shape[0]} samples")
        else:
            self.results['warnings'].append("⚠ NLP dataset is small or empty")
        
        # Check columns
        if 'disease' in df.columns and 'text' in df.columns:
            self.results['passed'].append("✓ Required columns present (disease, text)")
        else:
            self.results['failed'].append(f"✗ Missing columns. Found: {df.columns.tolist()}")
        
        # Check text quality
        if 'text' in df.columns:
            avg_length = df['text'].str.len().mean()
            print(f"Average text length: {avg_length:.1f} characters")
            
            if avg_length > 20:
                self.results['passed'].append("✓ Text samples have reasonable length")
            else:
                self.results['warnings'].append("⚠ Text samples are very short")
            
            # Check for empty texts
            empty_texts = df['text'].isna().sum()
            if empty_texts == 0:
                self.results['passed'].append("✓ No empty text samples")
            else:
                self.results['warnings'].append(f"⚠ {empty_texts} empty text samples")
    
    def verify_disease_registry(self):
        """Verify disease registry."""
        print("\n" + "="*60)
        print("VERIFYING DISEASE REGISTRY")
        print("="*60)
        
        filepath = 'datasets/disease_registry.csv'
        if not self.check_file_exists(filepath):
            return
        
        df = pd.read_csv(filepath)
        
        # Check shape
        print(f"\nShape: {df.shape}")
        if df.shape[0] == 50:
            self.results['passed'].append("✓ Registry has 50 diseases")
        else:
            self.results['warnings'].append(f"⚠ Expected 50 diseases, got {df.shape[0]}")
        
        # Check columns
        expected_cols = ['disease', 'has_structured_data', 'has_nlp_data', 
                        'has_precautions', 'sample_count']
        if all(col in df.columns for col in expected_cols):
            self.results['passed'].append("✓ All expected columns present")
        else:
            self.results['failed'].append(f"✗ Missing columns. Found: {df.columns.tolist()}")
        
        # Check data availability
        print(f"\nData availability:")
        print(f"  Structured data: {df['has_structured_data'].sum()}/{len(df)}")
        print(f"  NLP data: {df['has_nlp_data'].sum()}/{len(df)}")
        print(f"  Precautions: {df['has_precautions'].sum()}/{len(df)}")
        
        if df['has_structured_data'].sum() == len(df):
            self.results['passed'].append("✓ All diseases have structured data")
        else:
            self.results['warnings'].append("⚠ Some diseases missing structured data")
    
    def verify_symptom_dictionary(self):
        """Verify symptom dictionary."""
        print("\n" + "="*60)
        print("VERIFYING SYMPTOM DICTIONARY")
        print("="*60)
        
        filepath = 'datasets/processed/symptom_dictionary.json'
        if not self.check_file_exists(filepath):
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Check structure
        if 'unique_symptoms' in data and 'symptom_mappings' in data:
            self.results['passed'].append("✓ Dictionary has required keys")
        else:
            self.results['failed'].append(f"✗ Missing keys. Found: {data.keys()}")
        
        # Check content
        if 'unique_symptoms' in data:
            num_symptoms = len(data['unique_symptoms'])
            print(f"\nUnique symptoms: {num_symptoms}")
            
            if num_symptoms > 100:
                self.results['passed'].append(f"✓ {num_symptoms} unique symptoms")
            else:
                self.results['warnings'].append(f"⚠ Only {num_symptoms} symptoms (expected more)")
        
        if 'symptom_mappings' in data:
            num_mappings = len(data['symptom_mappings'])
            print(f"Symptom mappings: {num_mappings}")
            self.results['passed'].append(f"✓ {num_mappings} symptom mappings")
    
    def verify_reports(self):
        """Verify generated reports."""
        print("\n" + "="*60)
        print("VERIFYING REPORTS")
        print("="*60)
        
        files = [
            'reports/preprocessing/preprocessing_summary.md',
            'reports/preprocessing/disease_distribution.png',
            'reports/preprocessing/symptom_frequency.png',
            'reports/preprocessing/data_quality_report.png'
        ]
        
        for filepath in files:
            self.check_file_exists(filepath)
    
    def print_summary(self):
        """Print verification summary."""
        print("\n" + "="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)
        
        print(f"\n✓ PASSED: {len(self.results['passed'])}")
        for item in self.results['passed']:
            print(f"  {item}")
        
        if self.results['warnings']:
            print(f"\n⚠ WARNINGS: {len(self.results['warnings'])}")
            for item in self.results['warnings']:
                print(f"  {item}")
        
        if self.results['failed']:
            print(f"\n✗ FAILED: {len(self.results['failed'])}")
            for item in self.results['failed']:
                print(f"  {item}")
        
        print("\n" + "="*70)
        
        if len(self.results['failed']) == 0:
            print("✓ ALL VERIFICATIONS PASSED")
            if len(self.results['warnings']) > 0:
                print(f"⚠ {len(self.results['warnings'])} warnings (non-critical)")
        else:
            print(f"✗ {len(self.results['failed'])} CRITICAL ISSUES FOUND")
        
        print("="*70)


def main():
    """Main verification function."""
    print("\n" + "="*70)
    print(" DATASET VERIFICATION")
    print(" Validating all generated datasets and reports")
    print("="*70)
    
    verifier = DatasetVerifier()
    
    # Verify all datasets
    verifier.verify_master_dataset()
    verifier.verify_ml_dataset()
    verifier.verify_nlp_dataset()
    verifier.verify_disease_registry()
    verifier.verify_symptom_dictionary()
    verifier.verify_reports()
    
    # Print summary
    verifier.print_summary()


if __name__ == "__main__":
    main()
