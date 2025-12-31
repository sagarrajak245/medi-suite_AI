"""
Medical Entity Schemas
Structured output from entity extraction agent
"""

from typing import List
from pydantic import BaseModel, Field


class StructuredMedicalEntities(BaseModel):
    """Structured medical entities for coding"""
    
    icd_terms: List[str] = Field(
        ...,
        description="Diagnostic terms relevant for ICD-10-CM coding "
                    "(diseases, symptoms, conditions, findings)"
    )
    
    cpt_terms: List[str] = Field(
        ...,
        description="Procedure and service terms relevant for CPT-4 coding "
                    "(tests, imaging, evaluations, treatments)"
    )
    
    hcpcs_terms: List[str] = Field(
        ...,
        description="Supply, medication, and equipment terms relevant for "
                    "HCPCS Level II coding"
    )
