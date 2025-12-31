"""
HCPCS Level II Coding Agent
Assigns HCPCS codes for supplies, drugs, and equipment using RAG
"""

from crewai import Agent, Task
from app.core.llm_config import llm_models
from app.tools.hcpcs_search_tool import HCPCS_Vector_Search_Tool
from app.models.hcpcs_models import HCPCSCodingOutput


def create_hcpcs_coding_agent() -> Agent:
    """Create the HCPCS Level II coding agent"""
    return Agent(
        role="HCPCS Level II Coding Agent",
        goal="Assign the most accurate HCPCS Level II codes for supplies, drugs, and equipment using RAG",
        backstory="""
        You are a certified HCPCS Level II medical coding specialist.

        Input:
        - Structured HCPCS-relevant terms (medications, supplies, DME, injections)
        - Associated ICD-10-CM diagnosis codes for medical necessity context

        You MUST:
        - Use the HCPCS vector search tool to retrieve relevant HCPCS references
        - Link each HCPCS code to one or more ICD-10-CM codes to justify medical necessity
        - Apply official HCPCS Level II and CMS coding guidelines
        - Distinguish drugs, supplies, DME, and non-physician services correctly
        - If retrieved HCPCS candidates do not contain the correct code or
          lack sufficient specificity, use your expert HCPCS coding knowledge
          to provide the most accurate Level II code
        - Return ONLY structured output conforming to the HCPCS output schema
        """,
        tools=[HCPCS_Vector_Search_Tool],
        max_rpm=20,
        max_iter=5,
        llm=llm_models.get_hcpcs_coding_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_hcpcs_coding_task(agent: Agent) -> Task:
    """Create the HCPCS Level II coding task"""
    return Task(
        name="HCPCS Coding Task",
        description="""
        You are given a list of structured HCPCS-relevant terms along with
        associated ICD-10-CM diagnosis codes.

        Perform the following steps:

        1. Call the HCPCS_Vector_Search_Tool ONCE, passing the full list
           of HCPCS-relevant terms together.
        2. Review the retrieved HCPCS Level II candidates for each term.
        3. Select the most accurate and most specific HCPCS code
           for each medication, supply, or piece of equipment.
        4. If the retrieved HCPCS candidates do not contain the correct code
           or lack sufficient specificity, use your expert coding knowledge
           to provide the most accurate HCPCS Level II code.
        5. Link each selected HCPCS code to one or more ICD-10-CM diagnosis codes
           to justify its medical necessity.
        6. Apply official CMS and HCPCS Level II coding guidelines.
        7. Produce the final structured output.

        IMPORTANT:
        - Do NOT call the tool more than once.
        - Do NOT make repeated or per-term tool calls.
        - After receiving the tool output, return the final answer.
        """,
        expected_output="Structured HCPCS coding output conforming to the HCPCS_Coding_Output_Model model",
        agent=agent,
        output_pydantic=HCPCSCodingOutput
    )
