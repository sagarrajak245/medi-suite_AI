"""
ICD-10-CM Coding Agent
Assigns ICD-10-CM diagnosis codes using RAG
"""

from crewai import Agent, Task
from app.core.llm_config import llm_models
from app.tools.icd_search_tool import ICD_Vector_Search_Tool
from app.models.icd_models import ICDCodingOutput


def create_icd_coding_agent() -> Agent:
    """Create the ICD-10-CM coding agent"""
    return Agent(
        role="ICD-10-CM Coding Agent",
        goal="Assign the most accurate and specific ICD-10-CM diagnosis codes using RAG",
        backstory="""
        You are a certified ICD-10-CM medical coding specialist.

        Input:
        - Structured diagnostic terms extracted from clinical text.

        You MUST:
        - Use the ICD vector search tool to retrieve relevant ICD-10 references
        - Apply ICD-10-CM official coding guidelines
        - Prefer highest specificity
        - Ignore negated or ruled-out diagnoses
        - If the retrieved ICD-10-CM candidates do not contain the correct code or
          lack sufficient specificity, use your expert medical coding knowledge to provide
          the most accurate and specific ICD-10-CM code.
        - Return ONLY valid JSON matching the ICD output schema
        """,
        tools=[ICD_Vector_Search_Tool],
        max_rpm=20,
        max_iter=5,
        llm=llm_models.get_icd_coding_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_icd_coding_task(agent: Agent) -> Task:
    """Create the ICD-10-CM coding task"""
    return Task(
        name="ICD-10-CM Coding Task",
        description="""
        You are given a list of structured diagnostic terms for ICD-10-CM coding.

        Perform the following steps:

        1. Call the ICD_Vector_Search_Tool ONCE, passing the full list
           of diagnostic terms together.
        2. Review the retrieved ICD-10-CM candidates for each term.
        3. Select the most accurate and most specific ICD-10-CM code
           for each diagnostic term.
        4. If the retrieved ICD-10-CM candidates do not contain the correct code or lack sufficient specificity,
            use your expert medical coding knowledge to provide the most accurate and specific ICD-10-CM code.
        5. Apply official ICD-10-CM coding guidelines.
        6. Produce the final structured output.

        IMPORTANT:
        - Do NOT call the tool more than once.
        - Do NOT make repeated or per-term tool calls.
        - After receiving the tool output, return the final answer.
        """,
        expected_output="Structured ICD-10-CM coding output conforming to the ICD_Coding_Output_Model model",
        agent=agent,
        output_pydantic=ICDCodingOutput
    )
