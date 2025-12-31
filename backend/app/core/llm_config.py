"""
LLM Configuration
Initialize all LLM models used by CrewAI agents
"""

import os
from crewai import LLM
from app.core.config import settings


def setup_llm_environment():
    """Set up environment variables for LLM providers"""
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
    os.environ["OPENROUTER_API_KEY"] = settings.OPENROUTER_API_KEY


def get_kimi_k2() -> LLM:
    """Kimi K2 model via Groq - for ICD coding"""
    return LLM(model="groq/moonshotai/kimi-k2-instruct-0905")


def get_llama_4_maverick() -> LLM:
    """Llama 4 Maverick model via Groq"""
    return LLM(model="groq/meta-llama/llama-4-maverick-17b-128e-instruct")


def get_llama_3_3_70b() -> LLM:
    """Llama 3.3 70B model via Groq - for CPT coding (stable tool calling)"""
    return LLM(model="groq/llama-3.3-70b-versatile")


def get_gemini_flash() -> LLM:
    """Gemini 2.5 Flash model - for entity structuring"""
    return LLM(model="gemini/gemini-2.5-flash")


def get_xiaomi_mimo() -> LLM:
    """Xiaomi MIMO v2 Flash via OpenRouter - for HCPCS coding"""
    return LLM(model="openrouter/xiaomi/mimo-v2-flash:free")


# Initialize LLM instances (lazy loading)
class LLMModels:
    """Container for all LLM model instances"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        """Initialize all LLM models"""
        if not self._initialized:
            setup_llm_environment()
            self.gemini_flash = get_gemini_flash()
            self.kimi_k2 = get_kimi_k2()
            self.llama_3_3_70b = get_llama_3_3_70b()
            self.xiaomi_mimo = get_xiaomi_mimo()
            self._initialized = True
    
    def get_entity_structuring_llm(self) -> LLM:
        """LLM for entity structuring agent"""
        self.initialize()
        return self.gemini_flash
    
    def get_icd_coding_llm(self) -> LLM:
        """LLM for ICD coding agent"""
        self.initialize()
        return self.kimi_k2
    
    def get_cpt_coding_llm(self) -> LLM:
        """LLM for CPT coding agent"""
        self.initialize()
        return self.llama_3_3_70b
    
    def get_hcpcs_coding_llm(self) -> LLM:
        """LLM for HCPCS coding agent"""
        self.initialize()
        return self.xiaomi_mimo


# Global LLM models instance
llm_models = LLMModels()
