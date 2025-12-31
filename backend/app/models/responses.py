"""
API Response Schemas
Response models for API endpoints
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from app.models.entities import StructuredMedicalEntities
from app.models.icd_models import ICDCodingOutput
from app.models.cpt_models import CPTCodingOutput
from app.models.hcpcs_models import HCPCSCodingOutput
from app.models.judge_models import MedicalCodingJudgeOutput


class CodingResult(BaseModel):
    """Complete medical coding result"""
    
    entities: Optional[StructuredMedicalEntities] = Field(
        None, description="Extracted and structured medical entities"
    )
    
    icd_codes: Optional[ICDCodingOutput] = Field(
        None, description="ICD-10-CM diagnosis codes"
    )
    
    cpt_codes: Optional[CPTCodingOutput] = Field(
        None, description="CPT-4 procedure codes"
    )
    
    hcpcs_codes: Optional[HCPCSCodingOutput] = Field(
        None, description="HCPCS Level II codes"
    )


class PipelineResponse(BaseModel):
    """Complete pipeline response"""
    
    success: bool = Field(..., description="Whether the pipeline completed successfully")
    
    trace_id: Optional[str] = Field(
        None, description="Langfuse trace ID for this request"
    )
    
    coding_result: Optional[CodingResult] = Field(
        None, description="Medical coding results"
    )
    
    evaluation: Optional[MedicalCodingJudgeOutput] = Field(
        None, description="LLM judge evaluation results"
    )
    
    token_usage: Optional[Dict[str, Any]] = Field(
        None, description="Token usage statistics"
    )
    
    error: Optional[str] = Field(
        None, description="Error message if pipeline failed"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
