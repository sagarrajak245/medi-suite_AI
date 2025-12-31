"""
CPT-4 Coding Agent
Assigns CPT-4 procedure codes using RAG
"""

from crewai import Agent, Task
from app.core.llm_config import llm_models
from app.tools.cpt_search_tool import CPT_Vector_Search_Tool
from app.models.cpt_models import CPTCodingOutput


def create_cpt_coding_agent() -> Agent:
    """Create the CPT-4 coding agent"""
    return Agent(
        role="CPT-4 Coding Agent",
        goal="Assign the most accurate CPT-4 procedure and service codes using RAG",
        backstory="""
        You are a certified CPT-4 medical coding specialist.

        Input:
        - Structured procedure and service terms
        - Associated ICD-10-CM diagnosis codes for medical necessity context

        You MUST:
        - Use the CPT vector search tool to retrieve relevant CPT references
        - Apply official CPT-4 and AMA coding guidelines
        - Avoid unbundling and incorrect procedure hierarchy
        - Select the most accurate and specific CPT code
        - If retrieved CPT candidates do not contain the correct code or
          lack sufficient specificity, use your expert CPT coding knowledge
          to provide the most accurate CPT-4 code
        - Link each CPT code to one or more ICD-10-CM codes
        - Return ONLY structured output conforming to the CPT output schema
        """,
        tools=[CPT_Vector_Search_Tool],
        max_rpm=20,
        max_iter=5,
        llm=llm_models.get_cpt_coding_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_cpt_coding_task(agent: Agent) -> Task:
    """Create the CPT-4 coding task"""
    return Task(
        description="""
        You are given a list of structured procedure and service terms along with
        associated ICD-10-CM diagnosis codes.

        Perform the following steps:

        1. Call the CPT_Vector_Search_Tool ONCE, passing the full list
           of procedure and service terms together.
        2. Review the retrieved CPT-4 candidates for each term.
        3. Select the most accurate and most specific CPT code
           for each procedure or service.
        4. If the retrieved CPT candidates do not contain the correct code
           or lack sufficient specificity, use your expert CPT coding knowledge
           to provide the most accurate CPT-4 code.
        5. Link each selected CPT code to one or more ICD-10-CM diagnosis codes
           to justify medical necessity.
        6. Apply official AMA CPT-4 coding guidelines.
        7. Produce the final structured output.

        IMPORTANT:
        - Do NOT call the tool more than once.
        - Do NOT make repeated or per-term tool calls.
        - After receiving the tool output, return the final answer.
        """,
        expected_output="Structured CPT-4 coding output conforming to the CPT_Coding_Output_Model model",
        agent=agent,
        output_pydantic=CPTCodingOutput
    )
