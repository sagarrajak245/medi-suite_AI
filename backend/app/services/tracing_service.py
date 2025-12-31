"""
Tracing Service
Langfuse tracing and evaluation scoring
"""

import uuid
import datetime
from typing import Dict, Any, List, Optional
from app.core.observability import observability
from app.models.judge_models import MedicalCodingJudgeOutput


class TracingService:
    """Service for managing Langfuse tracing and scoring"""
    
    @staticmethod
    def create_trace_id() -> str:
        """Create a new unique trace ID"""
        seed = "custom-" + str(uuid.uuid4())
        return observability.create_trace_id(seed=seed)
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp string"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def add_evaluation_scores(
        evaluation_result: Dict[str, Any],
        trace_id: str
    ) -> None:
        """
        Add evaluation scores to Langfuse trace.
        
        Args:
            evaluation_result: Judge evaluation result dictionary
            trace_id: Langfuse trace ID
        """
        langfuse = observability.get_langfuse()
        
        # Overall numeric score
        langfuse.create_score(
            trace_id=trace_id,
            name="overall_score",
            value=evaluation_result["overall_score"],
            data_type="NUMERIC",
        )
        
        # Overall verdict (pass/fail)
        langfuse.create_score(
            trace_id=trace_id,
            name="overall_verdict",
            value=1 if evaluation_result["overall_verdict"].value == "pass" else 0,
            comment=evaluation_result.get("summary", ""),
        )
        
        # Compliance risk score
        risk_value = evaluation_result["compliance_risk"].value
        langfuse.create_score(
            trace_id=trace_id,
            name="compliance_risk",
            value={
                "low": 1.0,
                "medium": 0.5,
                "high": 0.0,
            }.get(risk_value, 0.5),
            comment=f"Risk Level: {risk_value}",
        )
        
        # Section-level scores
        for section_judge in evaluation_result["section_judgements"]:
            langfuse.create_score(
                trace_id=trace_id,
                name=f"section_{section_judge['section']}_verdict",
                value=1 if section_judge["verdict"].value == "pass" else 0,
                comment=section_judge.get("notes", ""),
            )
        
        # Code-level scores
        for code_judge in evaluation_result["code_judgements"]:
            code_name = f"code_{code_judge['code']}"
            code_type = code_judge["code_type"]
            
            # Documentation support score
            support_level = code_judge["documentation_support"].value
            support_score = {
                2: 1.0,  # FULLY_SUPPORTED
                1: 0.5,  # PARTIALLY_SUPPORTED
                0: 0.0,  # HALLUCINATED
            }.get(support_level, 0.0)
            
            langfuse.create_score(
                trace_id=trace_id,
                name=f"{code_name}_support",
                value=support_score,
                comment=(
                    f"Term match: {code_judge['term_match']}, "
                    f"Issues: {code_judge.get('issues', 'None')}"
                ),
            )
            
            # Linkage validity (if applicable)
            if code_judge.get("linkage_valid") is not None:
                langfuse.create_score(
                    trace_id=trace_id,
                    name=f"{code_type}_{code_name}_linkage",
                    value=1 if code_judge["linkage_valid"] else 0,
                )


# Singleton instance
tracing_service = TracingService()
