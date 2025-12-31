"""
Custom Exception Classes
API and service layer exceptions
"""

from fastapi import HTTPException, status


class MedicalCodingException(Exception):
    """Base exception for medical coding pipeline"""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class PDFExtractionError(MedicalCodingException):
    """Error during PDF text extraction"""
    pass


class EntityExtractionError(MedicalCodingException):
    """Error during medical entity extraction"""
    pass


class CodingAgentError(MedicalCodingException):
    """Error from coding agents (ICD, CPT, HCPCS)"""
    pass


class VectorSearchError(MedicalCodingException):
    """Error during vector database search"""
    pass


class EvaluationError(MedicalCodingException):
    """Error during LLM judge evaluation"""
    pass


# HTTP Exception helpers
def raise_bad_request(message: str):
    """Raise 400 Bad Request"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def raise_not_found(message: str):
    """Raise 404 Not Found"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )


def raise_internal_error(message: str):
    """Raise 500 Internal Server Error"""
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=message
    )
