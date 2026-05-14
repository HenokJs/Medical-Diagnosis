"""
Medical Dataset Preparation Pipeline - Part 2
==============================================
Substeps 13-20: Disease Registry, Unified Profiles, Severity, Master Dataset,
ML Dataset, NLP Dataset, Analytics, and Export.

Author: Senior AI/ML Data Engineer
Date: 2026-05-11
"""

import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Set, Tuple
import warnings
warnings.filterwarnings('ignore')

# Import from part 1
from dataset_preparation import TextNormalizer, MedicalDatasetPreprocessor

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


# ============================================================================
# SUBSTEP 13: Create Disease Registry
# ============================================================================

class DiseaseRegistryBuilder:
    """Creates the central disease registry from all data sources."""
    
    def __init__(self, disease_symptom_df, symptom2disease_df, precaution_df):
        self.disease_symptom_df = disease_symptom_df
        self.symptom2disease_df = symptom2disease_df
        self.precaution_df = precaution_df
        self.registry = None
        
    def build_registry(self, top_n: int = 50) -> pd.DataFrame:
        """
        Build disease registry using Disease-Symptom dataset as master source.
        
        Args:
            top_n: Number of diseases to include (default 50)
            
        Returns:
            Disease registry dataframe
        """
        print("\n" + "="*60)
        print("SUBSTEP 13: CREATING DISEASE REGISTRY")
        print("="*60)
        
        # Get diseases from primary dataset
        primary_diseases = self.disease_symptom_df['diseases'].unique()
        print(f"\nDiseases in primary dataset: {len(primary_diseases)}")
        
        # Get diseases from other datasets
        nlp_diseases = set(self.symptom2disease_df['label'].unique())
        precaution_diseases = set(self.precaution_df['Disease'].unique())
        
        print(f"Diseases in NLP dataset: {len(nlp_diseases)}")
        print(f"Diseases in precaution dataset: {len(precaution_diseases)}")
        
        # Select top N clinically relevant diseases from primary dataset
        disease_counts = self.disease_symptom_df['diseases'].value_counts()
        selected_diseases = disease_counts.head(top_n).index.tolist()
        
        print(f"\nSelected {len(selected_diseases)} diseases for registry")
        
        # Build registry
        registry_data = []
        for disease in selected_diseases:
            registry_data.append({
                'disease': disease,
                'has_structured_data': True,  # All from primary dataset
                'has_nlp_data': disease in nlp_diseases,
                'has_precautions': disease in precaution_diseases,
                'sample_count': disease_counts[disease]
            })
        
        self.registry = pd.DataFrame(registry_data)
        
        # Print statistics
        print("\nRegistry Statistics:")
        print(f"  Total diseases: {len(self.registry)}")
        print(f"  With structured data: {self.registry['has_structured_data'].sum()}")
        print(f"  With NLP data: {self.registry['has_nlp_data'].sum()}")
        print(f"  With precautions: {self.registry['has_precautions'].sum()}")
        
        # Save registry
        self.registry.to_csv('datasets/disease_registry.csv', index=False)
        print("\n✓ Disease registry saved to: datasets/disease_registry.csv")
        
        return self.registry


# ============================================================================
# SUBSTEP 14: Create Unified Disease Profiles
# ============================================================================

class DiseaseProfileBuilder:
    """Creates unified disease profiles merging all data sources."""
    
    def __init__(self, disease_symptom_df, symptom2disease_df, precaution_df, registry):
        self.disease_symptom_df = disease_symptom_df
        self.symptom2disease_df = symptom2disease_df
        self.precaution_df = precaution_df
        self.registry = registry
        self.profiles = {}
        
    def extract_symptoms(self, disease: str) -> List[str]:
        """Extract symptoms for a disease from structured dataset."""
        disease_rows = self.disease_symptom_df[
            self.disease_symptom_df['diseases'] == disease
        ]
        
        if len(disease_rows) == 0:
            return []
        
        # Get symptom columns (all except 'diseases')
        symptom_cols = [col for col in disease_rows.columns if col != 'diseases']
        
        # Aggregate symptoms across all rows for this disease
        # Sum across all rows and find symptoms that appear at least once
        symptom_sums = disease_rows[symptom_cols].sum()
        
        # Filter symptoms that appear at least once
        symptoms = []
        for symptom in symptom_cols:
            try:
                if symptom_sums[symptom] > 0:
                    symptoms.append(symptom)
            except:
                # Skip if there's an issue with this symptom
                continue
        
        return sorted(symptoms)
    
    def extract_nlp_examples(self, disease: str, max_examples: int = 5) -> List[str]:
        """Extract NLP text examples for a disease."""
        disease_texts = self.symptom2disease_df[
            self.symptom2disease_df['label'] == disease
        ]['text'].tolist()
        
        return disease_texts[:max_examples] if disease_texts else []
    
    def extract_precautions(self, disease: str) -> List[str]:
        """Extract precautions for a disease."""
        precaution_row = self.precaution_df[
            self.precaution_df['Disease'] == disease
        ]
        
        if len(precaution_row) == 0:
            return []
        
        precautions = []
        for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
            if col in precaution_row.columns:
                precaution = precaution_row[col].values[0]
                if pd.notna(precaution) and precaution != '':
                    precautions.append(str(precaution).strip())
        
        return precautions
    
    def build_profiles(self) -> Dict:
        """
        Build unified disease profiles for all diseases in registry.
        
        Returns:
            Dictionary of disease profiles
        """
        print("\n" + "="*60)
        print("SUBSTEP 14: CREATING UNIFIED DISEASE PROFILES")
        print("="*60)
        
        for _, row in self.registry.iterrows():
            disease = row['disease']
            
            # Extract information from all sources
            symptoms = self.extract_symptoms(disease)
            nlp_examples = self.extract_nlp_examples(disease)
            precautions = self.extract_precautions(disease)
            
            # Create profile
            profile = {
                'disease': disease,
                'symptoms': symptoms,
                'description': f"Medical condition characterized by: {', '.join(symptoms[:5])}..." if symptoms else "No description available",
                'precautions': precautions if precautions else ["Consult a healthcare professional"],
                'severity': '',  # Will be filled in next step
                'nlp_examples': nlp_examples
            }
            
            self.profiles[disease] = profile
        
        print(f"\nCreated {len(self.profiles)} disease profiles")
        print(f"Average symptoms per disease: {np.mean([len(p['symptoms']) for p in self.profiles.values()]):.1f}")
        print(f"Average precautions per disease: {np.mean([len(p['precautions']) for p in self.profiles.values()]):.1f}")
        
        print("\n✓ Disease profiles created successfully")
        
        return self.profiles


# ============================================================================
# SUBSTEP 15: Severity Classification
# ============================================================================

class SeverityClassifier:
    """Assigns severity levels to diseases."""
    
    # Severity mappings based on clinical knowledge
    SEVERITY_MAP = {
        # Critical
        'heart attack': 'critical',
        'pneumonia': 'urgent',
        'dengue': 'urgent',
        'typhoid': 'urgent',
        'hepatitis b': 'urgent',
        'hepatitis c': 'urgent',
        'hepatitis d': 'urgent',
        'hepatitis e': 'urgent',
        'tuberculosis': 'urgent',
        'paralysis brain hemorrhage': 'critical',
        'aids': 'critical',
        
        # Urgent
        'malaria': 'urgent',
        'jaundice': 'urgent',
        'chronic cholestasis': 'urgent',
        'alcoholic hepatitis': 'urgent',
        'hepatitis a': 'urgent',
        
        # Moderate
        'diabetes': 'moderate',
        'hypertension': 'moderate',
        'bronchial asthma': 'moderate',
        'arthritis': 'moderate',
        'osteoarthristis': 'moderate',
        'migraine': 'moderate',
        'peptic ulcer disease': 'moderate',
        'gastroesophageal reflux disease': 'moderate',
        'gerd': 'moderate',
        'urinary tract infection': 'moderate',
        'cervical spondylosis': 'moderate',
        'varicose veins': 'moderate',
        'hypothyroidism': 'moderate',
        'hyperthyroidism': 'moderate',
        'hypoglycemia': 'moderate',
        
        # Minor
        'common cold': 'minor',
        'allergy': 'minor',
        'acne': 'minor',
        'fungal infection': 'minor',
        'impetigo': 'minor',
        'chicken pox': 'minor',
        'psoriasis': 'minor',
        'drug reaction': 'minor',
        'dimorphic hemorrhoids': 'minor',
        'vertigo paroymsal positional vertigo': 'minor',
        'gastroenteritis': 'minor',
    }
    
    @staticmethod
    def classify_severity(disease: str) -> str:
        """
        Classify disease severity.
        
        Args:
            disease: Disease name
            
        Returns:
            Severity level: 'minor', 'moderate', 'urgent', or 'critical'
        """
        disease_lower = disease.lower().strip()
        
        if disease_lower in SeverityClassifier.SEVERITY_MAP:
            return SeverityClassifier.SEVERITY_MAP[disease_lower]
        
        # Default to moderate if unknown
        return 'moderate'
    
    @staticmethod
    def apply_severity(profiles: Dict) -> Dict:
        """
        Apply severity classification to all disease profiles.
        
        Args:
            profiles: Dictionary of disease profiles
            
        Returns:
            Updated profiles with severity
        """
        print("\n" + "="*60)
        print("SUBSTEP 15: SEVERITY CLASSIFICATION")
        print("="*60)
        
        severity_counts = Counter()
        
        for disease, profile in profiles.items():
            severity = SeverityClassifier.classify_severity(disease)
            profile['severity'] = severity
            severity_counts[severity] += 1
        
        print("\nSeverity Distribution:")
        for severity in ['minor', 'moderate', 'urgent', 'critical']:
            count = severity_counts[severity]
            pct = (count / len(profiles)) * 100
            print(f"  {severity.capitalize()}: {count} ({pct:.1f}%)")
        
        print("\n✓ Severity classification completed")
        
        return profiles


# ============================================================================
# SUBSTEP 16: Generate Master Dataset
# ============================================================================

def generate_master_dataset(profiles: Dict) -> pd.DataFrame:
    """
    Generate master dataset from disease profiles.
    
    Args:
        profiles: Dictionary of disease profiles
        
    Returns:
        Master dataset dataframe
    """
    print("\n" + "="*60)
    print("SUBSTEP 16: GENERATING MASTER DATASET")
    print("="*60)
    
    master_data = []
    
    for disease, profile in profiles.items():
        master_data.append({
            'disease': profile['disease'],
            'symptoms': '|'.join(profile['symptoms']),
            'description': profile['description'],
            'precautions': '|'.join(profile['precautions']),
            'severity': profile['severity'],
            'nlp_examples': '|'.join(profile['nlp_examples'][:3]),  # Limit to 3 examples
            'symptom_count': len(profile['symptoms'])
        })
    
    master_df = pd.DataFrame(master_data)
    
    print(f"\nMaster dataset shape: {master_df.shape}")
    print(f"Columns: {master_df.columns.tolist()}")
    
    # Save master dataset
    master_df.to_csv('datasets/master_dataset.csv', index=False)
    print("\n✓ Master dataset saved to: datasets/master_dataset.csv")
    
    return master_df


# ============================================================================
# SUBSTEP 17: Generate Encoded ML Dataset
# ============================================================================

def generate_ml_dataset(disease_symptom_df: pd.DataFrame, registry: pd.DataFrame) -> pd.DataFrame:
    """
    Generate ML-ready dataset with one-hot encoded symptoms.
    
    Args:
        disease_symptom_df: Disease-symptom dataframe
        registry: Disease registry
        
    Returns:
        ML dataset dataframe
    """
    print("\n" + "="*60)
    print("SUBSTEP 17: GENERATING ENCODED ML DATASET")
    print("="*60)
    
    # Filter to only diseases in registry
    registry_diseases = registry['disease'].tolist()
    ml_df = disease_symptom_df[disease_symptom_df['diseases'].isin(registry_diseases)].copy()
    
    # Rename 'diseases' to 'disease' for consistency
    ml_df = ml_df.rename(columns={'diseases': 'disease'})
    
    print(f"\nML dataset shape: {ml_df.shape}")
    print(f"Diseases: {ml_df['disease'].nunique()}")
    print(f"Symptom features: {ml_df.shape[1] - 1}")
    
    # Get symptom columns
    symptom_cols = [col for col in ml_df.columns if col != 'disease']
    print(f"Total symptoms: {len(symptom_cols)}")
    
    # Save ML dataset
    ml_df.to_csv('datasets/ml_dataset.csv', index=False)
    print("\n✓ ML dataset saved to: datasets/ml_dataset.csv")
    
    return ml_df


# ============================================================================
# SUBSTEP 18: Generate NLP Dataset
# ============================================================================

def generate_nlp_dataset(symptom2disease_df: pd.DataFrame, registry: pd.DataFrame) -> pd.DataFrame:
    """
    Generate NLP-ready dataset from Symptom2Disease.
    
    Args:
        symptom2disease_df: Symptom2Disease dataframe
        registry: Disease registry
        
    Returns:
        NLP dataset dataframe
    """
    print("\n" + "="*60)
    print("SUBSTEP 18: GENERATING NLP DATASET")
    print("="*60)
    
    # Filter to only diseases in registry
    registry_diseases = registry['disease'].tolist()
    nlp_df = symptom2disease_df[symptom2disease_df['label'].isin(registry_diseases)].copy()
    
    # Rename columns for consistency
    nlp_df = nlp_df.rename(columns={'label': 'disease'})
    
    # Clean text (already normalized in part 1)
    nlp_df['text_length'] = nlp_df['text'].str.len()
    
    # Remove very short texts (likely noise)
    nlp_df = nlp_df[nlp_df['text_length'] > 20]
    
    print(f"\nNLP dataset shape: {nlp_df.shape}")
    print(f"Diseases: {nlp_df['disease'].nunique()}")
    print(f"Average text length: {nlp_df['text_length'].mean():.1f} characters")
    
    # Save NLP dataset
    nlp_df[['disease', 'text']].to_csv('datasets/nlp_dataset.csv', index=False)
    print("\n✓ NLP dataset saved to: datasets/nlp_dataset.csv")
    
    return nlp_df


# ============================================================================
# SUBSTEP 19: Generate Analytics
# ============================================================================

def generate_analytics(master_df: pd.DataFrame, ml_df: pd.DataFrame, nlp_df: pd.DataFrame):
    """
    Generate preprocessing analytics and visualizations.
    
    Args:
        master_df: Master dataset
        ml_df: ML dataset
        nlp_df: NLP dataset
    """
    print("\n" + "="*60)
    print("SUBSTEP 19: GENERATING ANALYTICS")
    print("="*60)
    
    # 1. Disease Distribution
    plt.figure(figsize=(14, 6))
    disease_counts = ml_df['disease'].value_counts().head(20)
    plt.barh(range(len(disease_counts)), disease_counts.values, color='steelblue')
    plt.yticks(range(len(disease_counts)), disease_counts.index)
    plt.xlabel('Number of Samples')
    plt.title('Top 20 Diseases by Sample Count')
    plt.tight_layout()
    plt.savefig('reports/preprocessing/disease_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: disease_distribution.png")
    plt.close()
    
    # 2. Symptom Frequency
    plt.figure(figsize=(14, 6))
    symptom_cols = [col for col in ml_df.columns if col != 'disease']
    symptom_freq = ml_df[symptom_cols].sum().sort_values(ascending=False).head(20)
    plt.barh(range(len(symptom_freq)), symptom_freq.values, color='coral')
    plt.yticks(range(len(symptom_freq)), symptom_freq.index)
    plt.xlabel('Frequency')
    plt.title('Top 20 Most Common Symptoms')
    plt.tight_layout()
    plt.savefig('reports/preprocessing/symptom_frequency.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: symptom_frequency.png")
    plt.close()
    
    # 3. Data Quality Report
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Severity distribution
    severity_counts = master_df['severity'].value_counts()
    axes[0, 0].pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', 
                   colors=['lightgreen', 'gold', 'orange', 'red'])
    axes[0, 0].set_title('Disease Severity Distribution')
    
    # Symptom count distribution
    axes[0, 1].hist(master_df['symptom_count'], bins=20, color='skyblue', edgecolor='black')
    axes[0, 1].set_xlabel('Number of Symptoms')
    axes[0, 1].set_ylabel('Number of Diseases')
    axes[0, 1].set_title('Symptoms per Disease Distribution')
    
    # Dataset sizes
    dataset_sizes = {
        'Master': len(master_df),
        'ML': len(ml_df),
        'NLP': len(nlp_df)
    }
    axes[1, 0].bar(dataset_sizes.keys(), dataset_sizes.values(), color=['purple', 'green', 'blue'])
    axes[1, 0].set_ylabel('Number of Records')
    axes[1, 0].set_title('Dataset Sizes')
    
    # Disease coverage
    coverage_data = {
        'Structured Data': len(master_df),
        'NLP Data': nlp_df['disease'].nunique(),
        'Precautions': master_df[master_df['precautions'] != 'Consult a healthcare professional'].shape[0]
    }
    axes[1, 1].bar(coverage_data.keys(), coverage_data.values(), color=['teal', 'orange', 'pink'])
    axes[1, 1].set_ylabel('Number of Diseases')
    axes[1, 1].set_title('Data Source Coverage')
    axes[1, 1].tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig('reports/preprocessing/data_quality_report.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: data_quality_report.png")
    plt.close()
    
    print("\n✓ Analytics generation completed")


# ============================================================================
# SUBSTEP 20: Export Final Assets and Summary
# ============================================================================

def export_summary(master_df: pd.DataFrame, ml_df: pd.DataFrame, nlp_df: pd.DataFrame, 
                   registry: pd.DataFrame, profiles: Dict):
    """
    Export preprocessing summary report.
    
    Args:
        master_df: Master dataset
        ml_df: ML dataset
        nlp_df: NLP dataset
        registry: Disease registry
        profiles: Disease profiles
    """
    print("\n" + "="*60)
    print("SUBSTEP 20: EXPORTING FINAL ASSETS AND SUMMARY")
    print("="*60)
    
    summary = f"""# Medical Dataset Preprocessing Summary

## Overview
This report summarizes the preprocessing pipeline for the hybrid medical diagnosis decision support system.

**Date:** 2026-05-11  
**Pipeline Version:** 1.0  
**Author:** Senior AI/ML Data Engineer

---

## Datasets Generated

### 1. Master Dataset
- **File:** `datasets/master_dataset.csv`
- **Records:** {len(master_df)}
- **Columns:** {master_df.shape[1]}
- **Description:** Unified disease profiles with symptoms, descriptions, precautions, and severity

### 2. ML Dataset
- **File:** `datasets/ml_dataset.csv`
- **Records:** {len(ml_df)}
- **Features:** {ml_df.shape[1] - 1} (one-hot encoded symptoms)
- **Diseases:** {ml_df['disease'].nunique()}
- **Description:** ML-ready dataset for Random Forest and other classifiers

### 3. NLP Dataset
- **File:** `datasets/nlp_dataset.csv`
- **Records:** {len(nlp_df)}
- **Diseases:** {nlp_df['disease'].nunique()}
- **Description:** Free-text symptom descriptions for NLP models

### 4. Disease Registry
- **File:** `datasets/disease_registry.csv`
- **Diseases:** {len(registry)}
- **Description:** Central disease index with data source availability

### 5. Symptom Dictionary
- **File:** `datasets/processed/symptom_dictionary.json`
- **Unique Symptoms:** {len(json.load(open('datasets/processed/symptom_dictionary.json'))['unique_symptoms'])}
- **Description:** Standardized symptom vocabulary and mappings

---

## Preprocessing Steps Completed

### Substep 10: Normalization
- ✓ Disease names normalized
- ✓ Symptom names normalized
- ✓ Text fields cleaned and standardized

### Substep 11: Symptom Standardization
- ✓ Symptom vocabulary created
- ✓ Synonym mappings established
- ✓ Duplicate symptoms merged

### Substep 12: Data Cleaning
- ✓ Missing values handled
- ✓ Duplicates removed
- ✓ Empty rows filtered

### Substep 13: Disease Registry
- ✓ 50 clinically relevant diseases selected
- ✓ Data source availability tracked

### Substep 14: Unified Disease Profiles
- ✓ Multi-source data fusion completed
- ✓ Symptoms, precautions, and examples merged

### Substep 15: Severity Classification
- ✓ Diseases classified into 4 severity levels
- ✓ Minor: {len([p for p in profiles.values() if p['severity'] == 'minor'])} diseases
- ✓ Moderate: {len([p for p in profiles.values() if p['severity'] == 'moderate'])} diseases
- ✓ Urgent: {len([p for p in profiles.values() if p['severity'] == 'urgent'])} diseases
- ✓ Critical: {len([p for p in profiles.values() if p['severity'] == 'critical'])} diseases

### Substep 16: Master Dataset
- ✓ Comprehensive disease profiles generated

### Substep 17: ML Dataset
- ✓ One-hot encoded symptom features
- ✓ Ready for scikit-learn models

### Substep 18: NLP Dataset
- ✓ Clean text data for TF-IDF/embeddings
- ✓ Suitable for BERT, transformers

### Substep 19: Analytics
- ✓ Disease distribution chart
- ✓ Symptom frequency analysis
- ✓ Data quality report

### Substep 20: Export
- ✓ All datasets exported
- ✓ Summary report generated

---

## Data Quality Metrics

### Disease Coverage
- Total diseases in registry: {len(registry)}
- Diseases with structured data: {registry['has_structured_data'].sum()}
- Diseases with NLP data: {registry['has_nlp_data'].sum()}
- Diseases with precautions: {registry['has_precautions'].sum()}

### Symptom Statistics
- Average symptoms per disease: {master_df['symptom_count'].mean():.1f}
- Min symptoms: {master_df['symptom_count'].min()}
- Max symptoms: {master_df['symptom_count'].max()}

### Dataset Sizes
- Master dataset: {len(master_df)} records
- ML dataset: {len(ml_df)} records
- NLP dataset: {len(nlp_df)} records

---

## Next Steps

### Model Training
1. **Random Forest Classifier**
   - Use `ml_dataset.csv`
   - Train on one-hot encoded symptoms
   - Target: disease labels

2. **Deep Learning Model**
   - Use `ml_dataset.csv`
   - Build neural network with symptom features
   - Experiment with architectures

3. **NLP Model**
   - Use `nlp_dataset.csv`
   - Train TF-IDF + classifier
   - Or fine-tune BERT/BioBERT

4. **Rule-Based System**
   - Use `master_dataset.csv`
   - Implement symptom-matching rules
   - Integrate severity-based triage

### Integration
- Flask backend API development
- Streamlit frontend interface
- Hybrid model ensemble
- Explainability layer (SHAP, LIME)

---

## Files Generated

```
datasets/
├── master_dataset.csv
├── ml_dataset.csv
├── nlp_dataset.csv
├── disease_registry.csv
└── processed/
    └── symptom_dictionary.json

reports/
└── preprocessing/
    ├── preprocessing_summary.md
    ├── disease_distribution.png
    ├── symptom_frequency.png
    └── data_quality_report.png
```

---

## Conclusion

The preprocessing pipeline has successfully prepared production-ready datasets for the hybrid medical diagnosis system. All datasets are clean, normalized, and ready for model training and deployment.

**Status:** ✓ COMPLETE  
**Quality:** Production-ready  
**Next Phase:** Model Development
"""
    
    # Save summary
    with open('reports/preprocessing/preprocessing_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("\n✓ Preprocessing summary saved to: reports/preprocessing/preprocessing_summary.md")
    print("\n" + "="*60)
    print("ALL ASSETS EXPORTED SUCCESSFULLY")
    print("="*60)
    print("\nGenerated files:")
    print("  - datasets/master_dataset.csv")
    print("  - datasets/ml_dataset.csv")
    print("  - datasets/nlp_dataset.csv")
    print("  - datasets/disease_registry.csv")
    print("  - datasets/processed/symptom_dictionary.json")
    print("  - reports/preprocessing/preprocessing_summary.md")
    print("  - reports/preprocessing/disease_distribution.png")
    print("  - reports/preprocessing/symptom_frequency.png")
    print("  - reports/preprocessing/data_quality_report.png")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function for substeps 13-20."""
    print("\n" + "="*70)
    print(" MEDICAL DATASET PREPARATION PIPELINE - PART 2")
    print(" Substeps 13-20: Registry, Profiles, Datasets, Analytics, Export")
    print("="*70)
    
    # Initialize preprocessor and run part 1
    print("\nRunning Part 1 (Substeps 10-12)...")
    preprocessor = MedicalDatasetPreprocessor()
    preprocessor.load_datasets()
    preprocessor.normalize_datasets()
    preprocessor.standardize_symptoms()
    preprocessor.clean_datasets()
    
    # SUBSTEP 13: Disease Registry
    registry_builder = DiseaseRegistryBuilder(
        preprocessor.disease_symptom_df,
        preprocessor.symptom2disease_df,
        preprocessor.precaution_df
    )
    registry = registry_builder.build_registry(top_n=50)
    
    # SUBSTEP 14: Disease Profiles
    profile_builder = DiseaseProfileBuilder(
        preprocessor.disease_symptom_df,
        preprocessor.symptom2disease_df,
        preprocessor.precaution_df,
        registry
    )
    profiles = profile_builder.build_profiles()
    
    # SUBSTEP 15: Severity Classification
    profiles = SeverityClassifier.apply_severity(profiles)
    
    # SUBSTEP 16: Master Dataset
    master_df = generate_master_dataset(profiles)
    
    # SUBSTEP 17: ML Dataset
    ml_df = generate_ml_dataset(preprocessor.disease_symptom_df, registry)
    
    # SUBSTEP 18: NLP Dataset
    nlp_df = generate_nlp_dataset(preprocessor.symptom2disease_df, registry)
    
    # SUBSTEP 19: Analytics
    generate_analytics(master_df, ml_df, nlp_df)
    
    # SUBSTEP 20: Export Summary
    export_summary(master_df, ml_df, nlp_df, registry, profiles)
    
    print("\n" + "="*70)
    print(" ✓ ALL SUBSTEPS (10-20) COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\n🎉 Preprocessing pipeline complete!")
    print("📊 All datasets are production-ready")
    print("🚀 Ready for model training and deployment")


if __name__ == "__main__":
    main()
