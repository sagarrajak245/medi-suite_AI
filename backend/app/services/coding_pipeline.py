"""
Medical Coding Pipeline Service
Main orchestration service for the entire coding pipeline
"""

from typing import Optional, Dict, Any, List
from langfuse import propagate_attributes
from app.core.observability import observability
from app.agents.crew import get_medical_coding_crew
from app.services.pdf_extractor import pdf_extractor
from app.services.judge_service import judge_service
from app.services.tracing_service import tracing_service
from app.utils.text_utils import preprocess_medical_text
from app.utils.exceptions import MedicalCodingException
from app.models.responses import CodingResult, PipelineResponse
from app.models.entities import StructuredMedicalEntities
from app.models.icd_models import ICDCodingOutput
from app.models.cpt_models import CPTCodingOutput
from app.models.hcpcs_models import HCPCSCodingOutput


class CodingPipelineService:
    """Main service for orchestrating the medical coding pipeline"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.crew = get_medical_coding_crew(verbose=verbose)
    
    def process_text(
        self,
        medical_report_text: str,
        include_evaluation: bool = True
    ) -> PipelineResponse:
        """
        Process medical text through the coding pipeline.
        
        Args:
            medical_report_text: Clinical text to process
            include_evaluation: Whether to run LLM judge evaluation
            
        Returns:
            PipelineResponse with all results
        """
        try:
            # Preprocess the text
            text = preprocess_medical_text(medical_report_text)
            
            # Create trace ID
            trace_id = tracing_service.create_trace_id()
            timestamp = tracing_service.get_timestamp()
            
            langfuse = observability.get_langfuse()
            
            # Run the crew pipeline with tracing
            with langfuse.start_as_current_observation(
                name='MEDICAL CODING MULTI AGENT CREW AI RAG ARCHITECTURE',
                as_type="span",
                trace_context={"trace_id": trace_id}
            ) as rag_span:
                with propagate_attributes(
                    trace_name="MEDICAL CODING PIPELINE",
                    user_id="api-user",
                    tags=["production", "crewai"],
                    metadata={
                        "timestamp": timestamp,
                        "environment": "production"
                    }
                ):
                    # Execute the crew
                    crew_output = self.crew.kickoff(text)
                    
                    # Parse task outputs
                    json_data = []
                    coding_result = CodingResult()
                    
                    for i, task_out in enumerate(crew_output.tasks_output):
                        if task_out.pydantic:
                            data = task_out.pydantic.model_dump()
                            json_data.append(data)
                            
                            # Map to coding result based on task order
                            if i == 0:  # Entity structuring
                                coding_result.entities = task_out.pydantic
                            elif i == 1:  # ICD coding
                                coding_result.icd_codes = task_out.pydantic
                            elif i == 2:  # HCPCS coding
                                coding_result.hcpcs_codes = task_out.pydantic
                            elif i == 3:  # CPT coding
                                coding_result.cpt_codes = task_out.pydantic
                    
                    # Update trace span
                    rag_span.update(
                        input=text,
                        output=json_data,
                        metadata={"token_usage": crew_output.token_usage}
                    )
            
            # Run evaluation if requested
            evaluation = None
            if include_evaluation and json_data:
                with langfuse.start_as_current_observation(
                    name='MEDICAL CODING JUDGE',
                    as_type="evaluator",
                    trace_context={"trace_id": trace_id}
                ) as judge_span:
                    with propagate_attributes(
                        trace_name="MEDICAL CODING PIPELINE",
                        user_id="api-user",
                        tags=["production", "judge"],
                        metadata={
                            "timestamp": timestamp,
                            "environment": "production"
                        }
                    ):
                        evaluation = judge_service.evaluate(
                            clinical_note=text,
                            coding_output=json_data
                        )
                        
                        # Add evaluation scores to trace
                        tracing_service.add_evaluation_scores(
                            evaluation.model_dump(),
                            trace_id
                        )
            
            return PipelineResponse(
                success=True,
                trace_id=trace_id,
                coding_result=coding_result,
                evaluation=evaluation,
                token_usage=crew_output.token_usage if hasattr(crew_output, 'token_usage') else None
            )
            
        except Exception as e:
            return PipelineResponse(
                success=False,
                error=str(e)
            )
    
    def process_pdf(
        self,
        pdf_path: str,
        include_evaluation: bool = True
    ) -> PipelineResponse:
        """
        Process a PDF file through the coding pipeline.
        
        Args:
            pdf_path: Path to the PDF file
            include_evaluation: Whether to run LLM judge evaluation
            
        Returns:
            PipelineResponse with all results
        """
        try:
            # Extract text from PDF
            text = pdf_extractor.extract_text_from_pdf(pdf_path)
            
            # Process through pipeline
            return self.process_text(text, include_evaluation)
            
        except Exception as e:
            return PipelineResponse(
                success=False,
                error=str(e)
            )
    
    def process_pdf_bytes(
        self,
        pdf_bytes: bytes,
        include_evaluation: bool = True
    ) -> PipelineResponse:
        """
        Process PDF bytes (from file upload) through the coding pipeline.
        
        Args:
            pdf_bytes: PDF file content as bytes
            include_evaluation: Whether to run LLM judge evaluation
            
        Returns:
            PipelineResponse with all results
        """
        try:
            # Extract text from PDF bytes
            text = pdf_extractor.extract_text_from_bytes(pdf_bytes)
            
            # Process through pipeline
            return self.process_text(text, include_evaluation)
            
        except Exception as e:
            return PipelineResponse(
                success=False,
                error=str(e)
            )


# Factory function
def get_coding_pipeline_service(verbose: bool = False) -> CodingPipelineService:
    """Get a coding pipeline service instance"""
    return CodingPipelineService(verbose=verbose)


# Singleton instance for dependency injection
coding_pipeline_service = CodingPipelineService(verbose=False)
