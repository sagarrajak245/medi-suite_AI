"""
Vector Database Configuration
Pinecone connection and index management
"""

import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.core.config import settings


class VectorDBManager:
    """Manages Pinecone vector database connections"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        """Initialize Pinecone connection and embedding model"""
        if not self._initialized:
            # Set Pinecone API key
            os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
            
            # Initialize Pinecone client
            self.pc = Pinecone()
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
            
            # Connect to indexes
            self._icd_index = None
            self._hcpcs_index = None
            self._cpt_index = None
            
            self._initialized = True
    
    @property
    def icd_index(self):
        """Get ICD-10 Pinecone index"""
        self.initialize()
        if self._icd_index is None:
            self._icd_index = self.pc.Index(settings.PINECONE_INDEX_ICD)
        return self._icd_index
    
    @property
    def hcpcs_index(self):
        """Get HCPCS Pinecone index"""
        self.initialize()
        if self._hcpcs_index is None:
            self._hcpcs_index = self.pc.Index(settings.PINECONE_INDEX_HCPCS)
        return self._hcpcs_index
    
    @property
    def cpt_index(self):
        """Get CPT Pinecone index"""
        self.initialize()
        if self._cpt_index is None:
            self._cpt_index = self.pc.Index(settings.PINECONE_INDEX_CPT)
        return self._cpt_index
    
    def get_embedding(self, text: str) -> list:
        """Generate embedding for given text"""
        self.initialize()
        embedding = self.embedding_model.encode(text)
        if hasattr(embedding, "tolist"):
            return embedding.tolist()
        return embedding


# Global vector DB manager instance
vector_db = VectorDBManager()
