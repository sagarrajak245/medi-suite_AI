"""
Utility Functions Module
"""

from app.utils.text_utils import clean_text, normalize_whitespace, preprocess_medical_text
from app.utils.compression import compress_vector_db_response, compress_icd_vector_db_response
from app.utils.exceptions import (
    MedicalCodingException,
    PDFExtractionError,
    EntityExtractionError,
    CodingAgentError,
    VectorSearchError,
    EvaluationError
)

__all__ = [
    # Text utils
    "clean_text", "normalize_whitespace", "preprocess_medical_text",
    # Compression
    "compress_vector_db_response", "compress_icd_vector_db_response",
    # Exceptions
    "MedicalCodingException", "PDFExtractionError", "EntityExtractionError",
    "CodingAgentError", "VectorSearchError", "EvaluationError"
]
