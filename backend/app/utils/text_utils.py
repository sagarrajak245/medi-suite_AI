"""
Text Cleaning Utilities
Text normalization and regex cleaning
"""

import re


def clean_text(text: str) -> str:
    """
    Remove non-ASCII and non-printable characters from text.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text with only ASCII printable characters
    """
    # Remove non-ASCII and non-printable characters
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize multiple whitespaces to single space.
    
    Args:
        text: Text with potential multiple whitespaces
        
    Returns:
        Text with normalized whitespace
    """
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def preprocess_medical_text(text: str) -> str:
    """
    Preprocess medical report text for processing.
    
    Args:
        text: Raw medical report text
        
    Returns:
        Preprocessed text ready for entity extraction
    """
    text = clean_text(text)
    text = normalize_whitespace(text)
    return text
