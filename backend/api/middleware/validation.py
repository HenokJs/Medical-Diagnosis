"""
Request Validation Middleware
==============================
Validate API requests.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from typing import Tuple, Dict, Any


def validate_diagnosis_request(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate diagnosis request data.
    
    Args:
        data: Request data dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"
    
    # Check for symptoms or free_text
    symptoms = data.get('symptoms', [])
    free_text = data.get('free_text', '')
    
    if not symptoms and not free_text:
        return False, "Either 'symptoms' array or 'free_text' is required"
    
    # Validate symptoms format
    if symptoms and not isinstance(symptoms, list):
        return False, "'symptoms' must be an array"
    
    # Validate age if provided
    age = data.get('age')
    if age is not None:
        if not isinstance(age, (int, float)):
            return False, "'age' must be a number"
        if age < 0 or age > 150:
            return False, "'age' must be between 0 and 150"
    
    # Validate gender if provided
    gender = data.get('gender')
    if gender is not None:
        if not isinstance(gender, str):
            return False, "'gender' must be a string"
        valid_genders = ['male', 'female', 'other', 'unknown']
        if gender.lower() not in valid_genders:
            return False, f"'gender' must be one of: {', '.join(valid_genders)}"
    
    # Validate duration_days if provided
    duration_days = data.get('duration_days')
    if duration_days is not None:
        if not isinstance(duration_days, (int, float)):
            return False, "'duration_days' must be a number"
        if duration_days < 0:
            return False, "'duration_days' must be non-negative"
    
    return True, ""


def validate_report_request(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate report generation request.
    
    Args:
        data: Request data dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"
    
    # Check required fields
    if 'diagnosis_result' not in data:
        return False, "'diagnosis_result' is required"
    
    if 'patient_info' not in data:
        return False, "'patient_info' is required"
    
    return True, ""
