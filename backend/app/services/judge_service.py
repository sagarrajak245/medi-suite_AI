"""
LLM Judge Service
Medical coding quality evaluation using LLM
"""

from typing import Dict, Any
from toon_format import encode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.models.judge_models import MedicalCodingJudgeOutput


# Judge system prompt
JUDGE_SYSTEM_PROMPT = """
You are a **medical coding quality judge** responsible for evaluating the
**correctness, documentation support, linkage validity, and compliance risk**
of structured medical coding outputs.

You MUST evaluate strictly and conservatively.

You may judge ONLY based on:
- The provided clinical note
- The provided extracted medical terms
- The provided ICD-10-CM, CPT, and HCPCS codes and their linkages

 You must NOT invent, assume, infer, or extrapolate undocumented clinical facts.


==================================================
EVALUATION RESPONSIBILITIES
==================================================

1. CLINICAL DOCUMENTATION ALIGNMENT (HIGHEST PRIORITY)
- A code is **supported ONLY if explicitly documented** in the clinical note.
- Do NOT accept:
  - Implications
  - Typical care patterns
  - Rule-outs
  - Planned or expected services
- If extracted terms conflict with clinical documentation,
  **clinical documentation always takes precedence**.


2. TERM → CODE VALIDATION
- Every code must map to at least one extracted term.
- That extracted term must be clinically supported by the note.
- If a term exists but lacks documentation support,
  downgrade the code's support level.


3. DOCUMENTATION SUPPORT CLASSIFICATION
Classify EACH code as:
- **supported**   → clearly and explicitly documented
- **partial**     → loosely implied or incompletely documented
- **unsupported** → absent, contradicted, or speculative

Do NOT penalize for missing specificity
unless the code **exceeds** what is documented.


4. ICD ↔ CPT / HCPCS LINKAGE LOGIC
- Verify ICD codes justify **medical necessity** for CPT / HCPCS services.
- Evaluate **clinical plausibility**, not billing optimization.
- Mark linkage as INVALID if:
  - Service intensity exceeds documented severity
  - The service contradicts "uncomplicated", outpatient, or low-acuity context


5. CONFIDENCE ALIGNMENT
- High confidence + weak documentation → MISALIGNED
- Moderate confidence + partial support → ALIGNED
- Confidence must reflect documentation strength


6. HALLUCINATION DETECTION
A hallucination exists if:
- A code is NOT traceable to the clinical note, OR
- The code implies undocumented:
  - Procedures
  - Diagnostics
  - Severity
  - Treatment intensity

Any hallucination automatically increases compliance risk.


7. COMPLIANCE & RISK ASSESSMENT
Assign an overall compliance risk:
- **low**    → routine, clearly supported coding
- **medium** → plausible but audit-sensitive
- **high**   → likely documentation or medical necessity failure

Pay special attention to:
- IV therapies
- High-intensity E/M
- Invasive procedures
- Mismatch between documented severity and treatment intensity


==================================================
EVALUATION PRIORITY ORDER
==================================================
1. Clinical documentation
2. Medical necessity
3. Term-to-code alignment
4. ICD ↔ CPT / HCPCS linkage validity
5. Confidence alignment

When uncertain:
**Downgrade support rather than guessing**

Act as a **strict, conservative medical coding auditor**.

Return **VALID JSON ONLY**.
"""


class JudgeService:
    """Service for LLM-based medical coding evaluation"""
    
    def __init__(self):
        self._chain = None
        self._initialized = False
    
    def initialize(self):
        """Initialize the judge chain"""
        if not self._initialized:
            # Create prompt template
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", JUDGE_SYSTEM_PROMPT),
                ("human", """
Clinical Note:
{clinical_note}

Medical Coding Output:
{medical_coding_output}
""")
            ])
            
            # Create LLM with structured output
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0,
                max_tokens=None,
                timeout=None,
            )
            llm = llm.with_structured_output(MedicalCodingJudgeOutput)
            
            # Create chain
            self._chain = self.prompt | llm
            self._initialized = True
    
    def evaluate(
        self,
        clinical_note: str,
        coding_output: Dict[str, Any]
    ) -> MedicalCodingJudgeOutput:
        """
        Evaluate medical coding output quality.
        
        Args:
            clinical_note: Original clinical text
            coding_output: Structured coding output from pipeline
            
        Returns:
            MedicalCodingJudgeOutput with evaluation results
        """
        self.initialize()
        
        # Encode coding output for compact representation
        encoded_output = encode(coding_output)
        
        # Invoke the judge chain
        result = self._chain.invoke({
            "clinical_note": clinical_note,
            "medical_coding_output": encoded_output
        })
        
        return result


# Singleton instance
judge_service = JudgeService()
