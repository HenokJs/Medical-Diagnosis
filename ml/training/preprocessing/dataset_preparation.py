"""
Medical Dataset Preparation Pipeline
=====================================
Complete preprocessing pipeline for hybrid medical diagnosis decision support system.
Implements Substeps 10-20: Normalization, Standardization, Cleaning, and Dataset Generation.

Author: Senior AI/ML Data Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import json
import re
import os
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Set, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# SUBSTEP 10: Normalize Disease and Symptom Names
# ============================================================================

class TextNormalizer:
    """Handles normalization of disease names, symptoms, and text fields."""
    
    # Disease name mappings (synonyms and variations)
    DISEASE_MAPPINGS = {
        'flu': 'influenza',
        'common cold': 'common cold',
        'cold': 'common cold',
        'gerd': 'gastroesophageal reflux disease',
        'gastroesophageal reflux disease': 'gastroesophageal reflux disease',
        'acid reflux': 'gastroesophageal reflux disease',
        'dimorphic hemorrhoids': 'dimorphic hemorrhoids',
        'piles': 'dimorphic hemorrhoids',
        'hemorrhoids': 'dimorphic hemorrhoids',
        'uti': 'urinary tract infection',
        'urinary tract infection': 'urinary tract infection',
        'peptic ulcer': 'peptic ulcer disease',
        'peptic ulcer disease': 'peptic ulcer disease',
        'drug reaction': 'drug reaction',
        'allergy': 'allergy',
        'allergic reaction': 'allergy',
        'diabetes': 'diabetes',
        'diabetes mellitus': 'diabetes',
        'hypertension': 'hypertension',
        'high blood pressure': 'hypertension',
        'migraine': 'migraine',
        'cervical spondylosis': 'cervical spondylosis',
        'jaundice': 'jaundice',
        'malaria': 'malaria',
        'typhoid': 'typhoid',
        'typhoid fever': 'typhoid',
        'chicken pox': 'chicken pox',
        'chickenpox': 'chicken pox',
        'varicose veins': 'varicose veins',
        'varicose vein': 'varicose veins',
        'fungal infection': 'fungal infection',
        'pneumonia': 'pneumonia',
        'arthritis': 'arthritis',
        'bronchial asthma': 'bronchial asthma',
        'asthma': 'bronchial asthma',
        'acne': 'acne',
        'psoriasis': 'psoriasis',
        'impetigo': 'impetigo',
        'dengue': 'dengue',
        'dengue fever': 'dengue',
    }
    
    # Symptom mappings (synonyms and variations)
    SYMPTOM_MAPPINGS = {
        'high temperature': 'fever',
        'high fever': 'fever',
        'elevated temperature': 'fever',
        'pyrexia': 'fever',
        'body ache': 'body pain',
        'body pain': 'body pain',
        'muscle ache': 'muscle pain',
        'muscle pain': 'muscle pain',
        'myalgia': 'muscle pain',
        'shortness of breath': 'breathing difficulty',
        'difficulty breathing': 'breathing difficulty',
        'breathlessness': 'breathing difficulty',
        'dyspnea': 'breathing difficulty',
        'tiredness': 'fatigue',
        'exhaustion': 'fatigue',
        'weakness': 'fatigue',
        'lethargy': 'fatigue',
        'stomach ache': 'abdominal pain',
        'belly pain': 'abdominal pain',
        'stomach pain': 'abdominal pain',
        'tummy ache': 'abdominal pain',
        'throwing up': 'vomiting',
        'puking': 'vomiting',
        'emesis': 'vomiting',
        'loose stools': 'diarrhea',
        'watery stools': 'diarrhea',
        'runny nose': 'nasal congestion',
        'stuffy nose': 'nasal congestion',
        'blocked nose': 'nasal congestion',
        'head pain': 'headache',
        'cephalalgia': 'headache',
        'feeling sick': 'nausea',
        'queasy': 'nausea',
        'skin eruption': 'skin rash',
        'rash': 'skin rash',
        'skin lesion': 'skin rash',
        'itchy skin': 'itching',
        'pruritus': 'itching',
        'scratching': 'itching',
        'joint ache': 'joint pain',
        'arthralgia': 'joint pain',
        'chills': 'chills',
        'shivering': 'chills',
        'rigor': 'chills',
        'constipation': 'constipation',
        'hard stools': 'constipation',
    }
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize general text: lowercase, remove extra whitespace, punctuation.
        
        Args:
            text: Input text string
            
        Returns:
            Normalized text string
        """
        if pd.isna(text) or text == '':
            return ''
        
        # Convert to string and lowercase
        text = str(text).lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        return text.strip()
    
    @staticmethod
    def normalize_disease(disease: str) -> str:
        """
        Normalize disease names using mapping dictionary.
        
        Args:
            disease: Disease name
            
        Returns:
            Normalized disease name
        """
        if pd.isna(disease) or disease == '':
            return ''
        
        # First apply general text normalization
        normalized = TextNormalizer.normalize_text(disease)
        
        # Apply disease-specific mappings
        if normalized in TextNormalizer.DISEASE_MAPPINGS:
            return TextNormalizer.DISEASE_MAPPINGS[normalized]
        
        return normalized
    
    @staticmethod
    def normalize_symptom(symptom: str) -> str:
        """
        Normalize symptom names using mapping dictionary.
        
        Args:
            symptom: Symptom name
            
        Returns:
            Normalized symptom name
        """
        if pd.isna(symptom) or symptom == '':
            return ''
        
        # First apply general text normalization
        normalized = TextNormalizer.normalize_text(symptom)
        
        # Apply symptom-specific mappings
        if normalized in TextNormalizer.SYMPTOM_MAPPINGS:
            return TextNormalizer.SYMPTOM_MAPPINGS[normalized]
        
        return normalized


# ============================================================================
# SUBSTEP 11: Symptom Standardization
# ============================================================================

class SymptomStandardizer:
    """Creates centralized symptom mapping and vocabulary."""
    
    def __init__(self):
        self.symptom_vocabulary: Set[str] = set()
        self.symptom_mappings: Dict[str, str] = {}
        
    def build_vocabulary(self, symptoms_list: List[str]) -> None:
        """
        Build unique symptom vocabulary from list of symptoms.
        
        Args:
            symptoms_list: List of symptom names
        """
        for symptom in symptoms_list:
            if symptom and symptom != '':
                normalized = TextNormalizer.normalize_symptom(symptom)
                if normalized:
                    self.symptom_vocabulary.add(normalized)
    
    def create_mappings(self) -> Dict[str, str]:
        """
        Create symptom mapping dictionary with synonyms.
        
        Returns:
            Dictionary mapping symptom variations to standard names
        """
        # Start with predefined mappings
        self.symptom_mappings = TextNormalizer.SYMPTOM_MAPPINGS.copy()
        
        # Add identity mappings for vocabulary
        for symptom in self.symptom_vocabulary:
            if symptom not in self.symptom_mappings:
                self.symptom_mappings[symptom] = symptom
        
        return self.symptom_mappings
    
    def get_unique_symptoms(self) -> List[str]:
        """Get sorted list of unique symptoms."""
        return sorted(list(self.symptom_vocabulary))


# ============================================================================
# SUBSTEP 12: Data Cleaning
# ============================================================================

class DataCleaner:
    """Handles missing values, duplicates, and invalid data."""
    
    def __init__(self):
        self.cleaning_stats = {
            'missing_values': {},
            'duplicates_removed': 0,
            'empty_rows_removed': 0,
            'invalid_diseases_removed': 0,
            'total_rows_before': 0,
            'total_rows_after': 0
        }
    
    def clean_dataset(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """
        Clean dataset: handle missing values, remove duplicates and empty rows.
        
        Args:
            df: Input dataframe
            dataset_name: Name of dataset for logging
            
        Returns:
            Cleaned dataframe
        """
        print(f"\n{'='*60}")
        print(f"Cleaning Dataset: {dataset_name}")
        print(f"{'='*60}")
        
        self.cleaning_stats['total_rows_before'] = len(df)
        print(f"Initial rows: {len(df)}")
        
        # Check missing values
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        self.cleaning_stats['missing_values'][dataset_name] = missing[missing > 0].to_dict()
        
        if missing.sum() > 0:
            print(f"\nMissing values found:")
            for col, count in missing[missing > 0].items():
                print(f"  - {col}: {count} ({missing_pct[col]:.2f}%)")
        
        # Remove completely empty rows
        before_empty = len(df)
        df = df.dropna(how='all')
        empty_removed = before_empty - len(df)
        self.cleaning_stats['empty_rows_removed'] += empty_removed
        if empty_removed > 0:
            print(f"\nRemoved {empty_removed} completely empty rows")
        
        # Remove duplicates
        before_dup = len(df)
        df = df.drop_duplicates()
        dup_removed = before_dup - len(df)
        self.cleaning_stats['duplicates_removed'] += dup_removed
        if dup_removed > 0:
            print(f"Removed {dup_removed} duplicate rows")
        
        self.cleaning_stats['total_rows_after'] = len(df)
        print(f"Final rows: {len(df)}")
        print(f"Rows removed: {self.cleaning_stats['total_rows_before'] - self.cleaning_stats['total_rows_after']}")
        
        return df
    
    def get_summary(self) -> Dict:
        """Get cleaning statistics summary."""
        return self.cleaning_stats


# ============================================================================
# Main Preprocessing Pipeline
# ============================================================================

class MedicalDatasetPreprocessor:
    """Main preprocessing pipeline orchestrator."""
    
    def __init__(self, raw_data_path: str = 'datasets/raw'):
        self.raw_data_path = raw_data_path
        self.normalizer = TextNormalizer()
        self.standardizer = SymptomStandardizer()
        self.cleaner = DataCleaner()
        
        # Datasets
        self.disease_symptom_df = None
        self.symptom2disease_df = None
        self.precaution_df = None
        
        # Processed data
        self.disease_registry = None
        self.master_dataset = None
        self.ml_dataset = None
        self.nlp_dataset = None
        
        # Create output directories
        os.makedirs('datasets/processed', exist_ok=True)
        os.makedirs('reports/preprocessing', exist_ok=True)
        
    def load_datasets(self):
        """Load all raw datasets."""
        print("\n" + "="*60)
        print("LOADING RAW DATASETS")
        print("="*60)
        
        # Load Disease-Symptom Dataset (PRIMARY)
        print("\nLoading Disease-Symptom Dataset (PRIMARY)...")
        self.disease_symptom_df = pd.read_csv(
            f'{self.raw_data_path}/Final_Augmented_dataset_Diseases_and_Symptoms.csv'
        )
        print(f"  Shape: {self.disease_symptom_df.shape}")
        print(f"  Diseases: {self.disease_symptom_df['diseases'].nunique()}")
        
        # Load Symptom2Disease Dataset (NLP)
        print("\nLoading Symptom2Disease Dataset (NLP)...")
        self.symptom2disease_df = pd.read_csv(
            f'{self.raw_data_path}/Symptom2Disease.csv'
        )
        print(f"  Shape: {self.symptom2disease_df.shape}")
        print(f"  Diseases: {self.symptom2disease_df['label'].nunique()}")
        
        # Load Precaution Dataset
        print("\nLoading Precaution Dataset...")
        self.precaution_df = pd.read_csv(
            f'{self.raw_data_path}/symptom_precaution.csv'
        )
        print(f"  Shape: {self.precaution_df.shape}")
        print(f"  Diseases: {self.precaution_df['Disease'].nunique()}")
        
        print("\n✓ All datasets loaded successfully")
    
    def normalize_datasets(self):
        """Apply normalization to all datasets (SUBSTEP 10)."""
        print("\n" + "="*60)
        print("SUBSTEP 10: NORMALIZING DISEASE AND SYMPTOM NAMES")
        print("="*60)
        
        # Normalize Disease-Symptom Dataset
        print("\nNormalizing Disease-Symptom Dataset...")
        self.disease_symptom_df['diseases'] = self.disease_symptom_df['diseases'].apply(
            self.normalizer.normalize_disease
        )
        
        # Normalize symptom column names
        symptom_cols = [col for col in self.disease_symptom_df.columns if col != 'diseases']
        normalized_cols = {col: self.normalizer.normalize_symptom(col) for col in symptom_cols}
        self.disease_symptom_df = self.disease_symptom_df.rename(columns=normalized_cols)
        
        # Normalize Symptom2Disease Dataset
        print("Normalizing Symptom2Disease Dataset...")
        self.symptom2disease_df['label'] = self.symptom2disease_df['label'].apply(
            self.normalizer.normalize_disease
        )
        self.symptom2disease_df['text'] = self.symptom2disease_df['text'].apply(
            self.normalizer.normalize_text
        )
        
        # Normalize Precaution Dataset
        print("Normalizing Precaution Dataset...")
        self.precaution_df['Disease'] = self.precaution_df['Disease'].apply(
            self.normalizer.normalize_disease
        )
        
        print("\n✓ Normalization completed")
    
    def standardize_symptoms(self):
        """Create symptom vocabulary and mappings (SUBSTEP 11)."""
        print("\n" + "="*60)
        print("SUBSTEP 11: SYMPTOM STANDARDIZATION")
        print("="*60)
        
        # Collect all symptoms from Disease-Symptom dataset
        symptom_cols = [col for col in self.disease_symptom_df.columns if col != 'diseases']
        self.standardizer.build_vocabulary(symptom_cols)
        
        # Create mappings
        symptom_mappings = self.standardizer.create_mappings()
        unique_symptoms = self.standardizer.get_unique_symptoms()
        
        print(f"\nTotal unique symptoms: {len(unique_symptoms)}")
        print(f"Symptom mappings created: {len(symptom_mappings)}")
        
        # Save symptom dictionary
        symptom_dict = {
            'unique_symptoms': unique_symptoms,
            'symptom_mappings': symptom_mappings,
            'total_count': len(unique_symptoms)
        }
        
        with open('datasets/processed/symptom_dictionary.json', 'w') as f:
            json.dump(symptom_dict, f, indent=2)
        
        print("\n✓ Symptom dictionary saved to: datasets/processed/symptom_dictionary.json")
    
    def clean_datasets(self):
        """Clean all datasets (SUBSTEP 12)."""
        print("\n" + "="*60)
        print("SUBSTEP 12: DATA CLEANING")
        print("="*60)
        
        # Clean each dataset
        self.disease_symptom_df = self.cleaner.clean_dataset(
            self.disease_symptom_df, 
            "Disease-Symptom"
        )
        
        self.symptom2disease_df = self.cleaner.clean_dataset(
            self.symptom2disease_df,
            "Symptom2Disease"
        )
        
        self.precaution_df = self.cleaner.clean_dataset(
            self.precaution_df,
            "Precaution"
        )
        
        # Print summary
        print("\n" + "="*60)
        print("CLEANING SUMMARY")
        print("="*60)
        stats = self.cleaner.get_summary()
        print(f"Total duplicates removed: {stats['duplicates_removed']}")
        print(f"Total empty rows removed: {stats['empty_rows_removed']}")
        
        print("\n✓ Data cleaning completed")


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print(" MEDICAL DATASET PREPARATION PIPELINE")
    print(" Substeps 10-12: Normalization, Standardization, and Cleaning")
    print("="*70)
    
    # Initialize preprocessor
    preprocessor = MedicalDatasetPreprocessor()
    
    # Execute pipeline
    preprocessor.load_datasets()
    preprocessor.normalize_datasets()
    preprocessor.standardize_symptoms()
    preprocessor.clean_datasets()
    
    print("\n" + "="*70)
    print(" ✓ SUBSTEPS 10-12 COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nNext: Run dataset_preparation_part2.py for Substeps 13-20")


if __name__ == "__main__":
    main()
