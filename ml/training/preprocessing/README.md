# Medical Dataset Preprocessing Pipeline

## Overview

This directory contains the complete preprocessing pipeline for the hybrid medical diagnosis decision support system. The pipeline implements **Substeps 10-20** of the dataset preparation workflow, transforming raw medical data into production-ready datasets for machine learning, deep learning, NLP, and rule-based inference.

## Architecture

The preprocessing pipeline follows a **knowledge-fusion approach**, where:
- **Disease-Symptom Dataset** is the PRIMARY dataset (246,945 records, 773 diseases)
- **Symptom2Disease Dataset** provides NLP enrichment (1,200 text examples, 24 diseases)
- **Precaution Dataset** adds clinical recommendations (41 diseases)

## Pipeline Components

### Part 1: Core Preprocessing (`dataset_preparation.py`)

**Substep 10: Normalization**
- `TextNormalizer` class handles disease and symptom name normalization
- Removes capitalization inconsistencies, whitespace, and punctuation
- Maps synonyms (e.g., "flu" → "influenza", "high fever" → "fever")

**Substep 11: Symptom Standardization**
- `SymptomStandardizer` creates centralized symptom vocabulary
- Merges synonymous symptoms and removes duplicates
- Generates `symptom_dictionary.json` with 374 unique symptoms

**Substep 12: Data Cleaning**
- `DataCleaner` handles missing values and duplicates
- Removed 57,298 duplicate rows from primary dataset
- Generates data quality statistics

### Part 2: Dataset Generation (`dataset_preparation_part2.py`)

**Substep 13: Disease Registry**
- `DiseaseRegistryBuilder` creates central disease index
- Selects 50 clinically relevant diseases
- Tracks data source availability

**Substep 14: Unified Disease Profiles**
- `DiseaseProfileBuilder` fuses multi-source data
- Extracts symptoms, precautions, and NLP examples
- Creates comprehensive disease profiles

**Substep 15: Severity Classification**
- `SeverityClassifier` assigns severity levels
- Categories: minor, moderate, urgent, critical
- Based on clinical knowledge

**Substep 16: Master Dataset**
- Generates unified disease profiles CSV
- Includes symptoms, descriptions, precautions, severity

**Substep 17: ML Dataset**
- One-hot encoded symptom features (377 features)
- 55,509 training samples across 50 diseases
- Ready for Random Forest, SVM, XGBoost

**Substep 18: NLP Dataset**
- Clean free-text symptom descriptions
- 100 text samples for 2 diseases
- Suitable for TF-IDF, BERT, transformers

**Substep 19: Analytics**
- Disease distribution visualization
- Symptom frequency analysis
- Data quality report

**Substep 20: Export**
- All datasets exported to CSV/JSON
- Comprehensive preprocessing summary
- Visualization charts

## Usage

### Running the Complete Pipeline

```bash
# Install dependencies
pip install -r requirements.txt

# Run the complete pipeline (Substeps 10-20)
python preprocessing/dataset_preparation_part2.py
```

### Running Individual Components

```bash
# Run only Substeps 10-12 (Normalization, Standardization, Cleaning)
python preprocessing/dataset_preparation.py
```

## Output Files

### Datasets
```
datasets/
├── master_dataset.csv              # 50 unified disease profiles
├── ml_dataset.csv                  # 55,509 ML-ready samples
├── nlp_dataset.csv                 # 100 NLP text samples
├── disease_registry.csv            # 50 disease index
└── processed/
    └── symptom_dictionary.json     # 374 unique symptoms
```

### Reports
```
reports/
└── preprocessing/
    ├── preprocessing_summary.md    # Complete pipeline summary
    ├── disease_distribution.png    # Top 20 diseases chart
    ├── symptom_frequency.png       # Top 20 symptoms chart
    └── data_quality_report.png     # 4-panel quality report
```

## Dataset Specifications

### Master Dataset (`master_dataset.csv`)
| Column | Type | Description |
|--------|------|-------------|
| disease | string | Normalized disease name |
| symptoms | string | Pipe-separated symptom list |
| description | string | Disease description |
| precautions | string | Pipe-separated precautions |
| severity | string | Severity level (minor/moderate/urgent/critical) |
| nlp_examples | string | Pipe-separated text examples |
| symptom_count | int | Number of symptoms |

### ML Dataset (`ml_dataset.csv`)
- **Shape:** 55,509 rows × 378 columns
- **Features:** 377 one-hot encoded symptoms
- **Target:** disease (50 classes)
- **Format:** Binary (0/1) for symptom presence

### NLP Dataset (`nlp_dataset.csv`)
| Column | Type | Description |
|--------|------|-------------|
| disease | string | Disease label |
| text | string | Normalized symptom description |

### Disease Registry (`disease_registry.csv`)
| Column | Type | Description |
|--------|------|-------------|
| disease | string | Disease name |
| has_structured_data | bool | Has ML features |
| has_nlp_data | bool | Has text examples |
| has_precautions | bool | Has clinical recommendations |
| sample_count | int | Number of training samples |

## Data Quality Metrics

- **Total Diseases:** 50 clinically relevant conditions
- **Total Symptoms:** 374 unique standardized symptoms
- **ML Training Samples:** 55,509 records
- **NLP Training Samples:** 100 text descriptions
- **Average Symptoms per Disease:** 11.1
- **Duplicates Removed:** 57,298 rows
- **Data Completeness:** 100% for structured data

## Severity Distribution

- **Minor:** 1 disease (2.0%)
- **Moderate:** 48 diseases (96.0%)
- **Urgent:** 1 disease (2.0%)
- **Critical:** 0 diseases (0.0%)

## Key Features

✅ **Modular Design:** Reusable classes and functions  
✅ **Production Quality:** Error handling, logging, validation  
✅ **Deterministic:** Reproducible results  
✅ **Scalable:** Handles large datasets efficiently  
✅ **Well-Documented:** Comprehensive docstrings and comments  
✅ **Type-Annotated:** Clear function signatures  
✅ **Tested:** Robust error handling  

## Next Steps

### Model Training
1. **Random Forest Classifier** - Use `ml_dataset.csv`
2. **Deep Neural Network** - Use `ml_dataset.csv`
3. **NLP Model (TF-IDF/BERT)** - Use `nlp_dataset.csv`
4. **Rule-Based System** - Use `master_dataset.csv`

### Integration
- Flask REST API backend
- Streamlit web interface
- Hybrid model ensemble
- SHAP/LIME explainability

## Technical Stack

- **Python 3.8+**
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization
- **seaborn** - Statistical plots
- **scikit-learn** - ML utilities

## Author

Senior AI/ML Data Engineer  
Date: 2026-05-11  
Version: 1.0

## License

This preprocessing pipeline is part of the Medical Diagnosis Decision Support System project.
