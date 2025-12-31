"""
CPT-4 Coding Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CPTCode(BaseModel):
    """Single CPT-4 code"""
    
    code: str = Field(..., description="CPT-4 procedure or service code")
    
    description: Optional[str] = Field(
        None, description="Official CPT description of the procedure or service"
    )
    
    linked_icd_codes: List[str] = Field(
        ...,
        description="List of ICD-10-CM diagnosis codes that justify the medical necessity "
                    "of this CPT procedure or service"
    )
    
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence score"
    )


class CPTCodingOutput(BaseModel):
    """CPT-4 coding output model"""
    
    cpt_codes: List[CPTCode] = Field(
        ..., description="List of CPT-4 codes linked to ICD-10 diagnoses"
    )
