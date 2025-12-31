"""
CrewAI Agents Module
"""

from app.agents.entity_structuring_agent import (
    create_entity_structuring_agent,
    create_entity_structuring_task
)
from app.agents.icd_coding_agent import (
    create_icd_coding_agent,
    create_icd_coding_task
)
from app.agents.cpt_coding_agent import (
    create_cpt_coding_agent,
    create_cpt_coding_task
)
from app.agents.hcpcs_coding_agent import (
    create_hcpcs_coding_agent,
    create_hcpcs_coding_task
)
from app.agents.crew import MedicalCodingCrew, get_medical_coding_crew

__all__ = [
    # Entity Structuring
    "create_entity_structuring_agent",
    "create_entity_structuring_task",
    # ICD Coding
    "create_icd_coding_agent",
    "create_icd_coding_task",
    # CPT Coding
    "create_cpt_coding_agent",
    "create_cpt_coding_task",
    # HCPCS Coding
    "create_hcpcs_coding_agent",
    "create_hcpcs_coding_task",
    # Crew
    "MedicalCodingCrew",
    "get_medical_coding_crew"
]
