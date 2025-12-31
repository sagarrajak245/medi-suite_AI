"""
FastAPI Dependencies
Dependency injection for services and configurations
"""

from functools import lru_cache
from app.core.config import Settings, get_settings
from app.core.vector_db import VectorDBManager, vector_db
from app.core.observability import ObservabilityManager, observability
from app.core.llm_config import LLMModels, llm_models


def get_config() -> Settings:
    """Dependency to get application settings"""
    return get_settings()


def get_vector_db() -> VectorDBManager:
    """Dependency to get vector database manager"""
    return vector_db


def get_observability() -> ObservabilityManager:
    """Dependency to get observability manager"""
    return observability


def get_llm_models() -> LLMModels:
    """Dependency to get LLM models"""
    return llm_models
