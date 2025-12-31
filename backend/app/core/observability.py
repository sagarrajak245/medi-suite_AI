"""
Observability Configuration
Langfuse and OpenLIT setup for tracing
"""

import os
import openlit
from langfuse import Langfuse
from app.core.config import settings


class ObservabilityManager:
    """Manages observability tools - Langfuse and OpenLIT"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        """Initialize observability tools"""
        if not self._initialized:
            # Set Langfuse environment variables
            os.environ['LANGFUSE_PUBLIC_KEY'] = settings.LANGFUSE_PUBLIC_KEY
            os.environ['LANGFUSE_SECRET_KEY'] = settings.LANGFUSE_SECRET_KEY
            os.environ['LANGFUSE_BASE_URL'] = settings.LANGFUSE_BASE_URL
            
            # Initialize Langfuse client
            self.langfuse = Langfuse()
            
            # Initialize OpenLIT
            openlit.init(
                disabled_instrumentors=[
                    "httpx", "requests", "transformers", 
                    "pinecone", "urllib3", "urllib", "langchain"
                ],
                disable_metrics=True,
                disable_batch=True
            )
            
            self._initialized = True
    
    def get_langfuse(self) -> Langfuse:
        """Get Langfuse client instance"""
        self.initialize()
        return self.langfuse
    
    def create_trace_id(self, seed: str = None) -> str:
        """Create a new trace ID"""
        self.initialize()
        import uuid
        if seed is None:
            seed = "custom-" + str(uuid.uuid4())
        return self.langfuse.create_trace_id(seed=seed)


# Global observability manager instance
observability = ObservabilityManager()
