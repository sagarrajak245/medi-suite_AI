"""
Medical Entity Structuring Agent
Extracts and structures medical entities from clinical text
"""

from crewai import Agent, Task
from app.core.llm_config import llm_models
from app.models.entities import StructuredMedicalEntities


def create_entity_structuring_agent() -> Agent:
    """Create the medical entity structuring agent"""
    return Agent(
        role="Medical Entity Structuring Agent",
        goal="Convert raw medical prescription content into coding-ready structured entities",
        backstory="""
        You are a medical coding pre-processor.
        You receive medical prescription content that may include:
        - Diagnoses or clinical impressions
        - Prescribed medications (drug name, dose, route, frequency)
        - Injections, infusions, or administered drugs
        - Procedures or services performed during the encounter
        - Clinically relevant findings that directly impact treatment

        Your responsibility is to analyze the prescription and
        extract, normalize, and categorize medically relevant information
        into coding-ready terms suitable for:
        - ICD-10-CM (diagnoses and clinically relevant conditions)
        - CPT-4 (procedures, evaluations, administrations)
        - HCPCS Level II (medications, injections, supplies, DME)

        return ONLY structured output conforming to the Structured_Medical_Entities model
        """,
        max_rpm=2,
        max_iter=5,
        verbose=True,
        allow_delegation=False,
        llm=llm_models.get_entity_structuring_llm()
    )


def create_entity_structuring_task(agent: Agent) -> Task:
    """Create the entity structuring task"""
    return Task(
        description="""
You are a medical coding entity extraction engine.

Process the following clinical encounter text:
{medical_report_text}

Your task is to extract **billing-relevant medical concepts** and organize them into the correct U.S. medical coding categories.

────────────────────────────────────────
OUTPUT STRUCTURE (MANDATORY)

Return THREE distinct structured lists:

1. ICD-10-CM Diagnostic Terms
2. CPT-4 Procedure / Service Terms
3. HCPCS Level II Terms (Drugs, Supplies, DME)

Return **terms only** (no codes, no explanations).

────────────────────────────────────────
EXTRACTION RULES (STRICT)

### 1. ICD-10-CM Diagnostic Terms
Extract conditions that meet ALL of the following:
- Explicitly documented as a diagnosis or assessment
- Not negated, denied, ruled out, or listed only as a possibility
- Clinically relevant to the current encounter

Include:
- Acute or chronic diseases
- Active conditions being treated
- Relevant historical conditions when documented as ongoing or impacting care

Exclude:
- Symptoms that are part of a confirmed diagnosis
- Normal exam findings
- Screening statements without a diagnosis

If no diagnosis is documented, extract **standalone symptoms** only.

Normalize abbreviations and shorthand to full clinical terms.

---

### 2. CPT-4 Procedure / Service Terms
Extract **only services that were actually performed during this encounter**, including:
- Evaluation & management services
- Laboratory tests performed
- Imaging studies completed
- Therapeutic procedures (e.g., infusions, injections)

Exclude:
- Planned, ordered, or future services
- Patient education or counseling alone
- Clinical observations without an associated service

Normalize descriptions to standard medical procedure terminology.

---

### 3. HCPCS Level II Terms
Extract **non-CPT billable items** that were **administered or provided during the encounter**, including:
- Injectable or infused medications
- Supplies or biological agents
- Durable medical equipment provided

Include:
- Medication name
- Route of administration
- Strength or dose when documented

Exclude:
- Oral medications that were only prescribed for home use
- Home medications not administered during the visit

────────────────────────────────────────
GENERAL NORMALIZATION RULES
- Ignore negated or irrelevant concepts
- Do not duplicate terms across categories
- Prefer specific diagnoses over vague findings
- Ensure each term clearly belongs to only one category
- Use medically standard terminology

────────────────────────────────────────
TERMINOLOGY PRECISION RULES (MANDATORY)

When extracting terms:

1. CPT-4 Terminology Precision
- Use conservative, minimally sufficient terminology.
- Do NOT assume higher specificity unless explicitly documented.
- If a test or procedure type is unclear:
  - Prefer general terms (e.g., "urinalysis, non-automated" rather than "urinalysis with microscopy").
- Only include qualifiers such as "with microscopy," "automated," "complex," or "extended"
  if explicitly stated in the clinical text.

2. E/M Service Terminology
- Extract E/M services at the category level only.
- Do NOT infer visit level or complexity.
- Use setting-neutral phrasing unless clearly documented.
  Examples:
  - "Evaluation and management service"
  - "Office or outpatient evaluation and management service" (only if setting is explicit)

3. HCPCS Medication Terminology
- Normalize medications using:
  Drug name + route + strength
- If administered via IV, prefer:
  "<drug>, intravenous infusion, <dose>"
- Do NOT assume bolus vs infusion unless explicitly stated.

4. Avoid Over-Specification
- When multiple interpretations are possible, select the least specific
  term that remains billing-relevant.
- Accuracy is preferred over granularity.
        """,
        expected_output="Structured output with ICD, CPT, HCPCS term lists",
        agent=agent,
        output_pydantic=StructuredMedicalEntities
    )
