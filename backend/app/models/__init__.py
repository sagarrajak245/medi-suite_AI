"""
Pydantic Models / Schemas
"""

from app.models.entities import StructuredMedicalEntities
from app.models.icd_models import ICDCode, ICDCodingOutput
from app.models.cpt_models import CPTCode, CPTCodingOutput
from app.models.hcpcs_models import HCPCSCode, HCPCSCodingOutput
from app.models.judge_models import (
    Verdict, SupportLevel, RiskLevel,
    CodeJudgement, SectionJudgement, MedicalCodingJudgeOutput
)
from app.models.requests import ProcessTextRequest, ProcessPDFRequest
from app.models.responses import CodingResult, PipelineResponse, HealthResponse

__all__ = [
    # Entities
    "StructuredMedicalEntities",
    # ICD
    "ICDCode", "ICDCodingOutput",
    # CPT
    "CPTCode", "CPTCodingOutput",
    # HCPCS
    "HCPCSCode", "HCPCSCodingOutput",
    # Judge
    "Verdict", "SupportLevel", "RiskLevel",
    "CodeJudgement", "SectionJudgement", "MedicalCodingJudgeOutput",
    # Requests
    "ProcessTextRequest", "ProcessPDFRequest",
    # Responses
    "CodingResult", "PipelineResponse", "HealthResponse"
]
