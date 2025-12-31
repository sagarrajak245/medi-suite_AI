"""
ICD-10-CM Coding Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ICDCode(BaseModel):
    """Single ICD-10-CM code"""
    
    code: str = Field(..., description="Standardized ICD-10-CM code")
    
    description: Optional[str] = Field(
        None, description="Official description of the code"
    )
    
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Model confidence score"
    )


class ICDCodingOutput(BaseModel):
    """ICD-10-CM coding output model"""
    
    icd_codes: List[ICDCode] = Field(
        ..., description="List of ICD-10-CM diagnosis codes"
    )
