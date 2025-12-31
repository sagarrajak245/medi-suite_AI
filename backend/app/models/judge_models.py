"""
Judge / Evaluation Schemas
LLM as Judge for medical coding quality evaluation
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Verdict(str, Enum):
    """Pass/fail verdict"""
    pass_ = "pass"
    fail = "fail"


class SupportLevel(Enum):
    """Documentation support level"""
    HALLUCINATED = 0
    PARTIALLY_SUPPORTED = 1
    FULLY_SUPPORTED = 2


class RiskLevel(str, Enum):
    """Compliance risk level"""
    low = "low"
    medium = "medium"
    high = "high"


class CodeJudgement(BaseModel):
    """Individual code evaluation"""
    
    code: str = Field(..., description="ICD, CPT, or HCPCS code")
    
    code_type: str = Field(..., description="icd | cpt | hcpcs")
    
    term_match: bool = Field(
        ..., description="Code matches extracted clinical term"
    )
    
    documentation_support: SupportLevel
    
    linkage_valid: Optional[bool] = Field(
        None,
        description="Whether linked ICD codes justify this code"
    )
    
    confidence_alignment: bool = Field(
        ..., description="Model confidence aligns with correctness"
    )
    
    issues: Optional[List[str]] = Field(
        default=None,
        description="Reasons for failure or concern"
    )


class SectionJudgement(BaseModel):
    """Section-level evaluation"""
    
    section: str = Field(..., description="icd | cpt | hcpcs")
    verdict: Verdict
    notes: Optional[str] = None


class MedicalCodingJudgeOutput(BaseModel):
    """Complete judge evaluation output"""
    
    overall_verdict: Verdict
    
    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall quality score"
    )
    
    section_judgements: List[SectionJudgement]
    
    code_judgements: List[CodeJudgement]
    
    compliance_risk: RiskLevel
    
    summary: str = Field(
        ..., min_length=30,
        description="Concise explanation of the final judgement"
    )
    
    notes: Optional[str] = None
