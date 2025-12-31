"""
Core module - Configuration, Settings, Dependencies
"""

from app.core.config import settings, get_settings
from app.core.llm_config import llm_models
from app.core.vector_db import vector_db
from app.core.observability import observability

__all__ = [
    "settings",
    "get_settings", 
    "llm_models",
    "vector_db",
    "observability"
]
