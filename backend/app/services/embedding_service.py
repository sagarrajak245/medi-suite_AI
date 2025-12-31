"""
Embedding Service
Generate embeddings using SentenceTransformer
"""

from typing import List
from app.core.vector_db import vector_db


class EmbeddingService:
    """Service for generating text embeddings"""
    
    @staticmethod
    def get_embedding(text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        return vector_db.get_embedding(text)
    
    @staticmethod
    def get_embeddings(texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        return [vector_db.get_embedding(text) for text in texts]


# Singleton instance
embedding_service = EmbeddingService()
