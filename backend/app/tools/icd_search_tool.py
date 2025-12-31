"""
ICD-10 Vector Search Tool
RAG tool for retrieving ICD-10-CM codes from Pinecone
"""

from typing import List
from crewai.tools import tool
from toon_format import encode
from app.core.vector_db import vector_db
from app.core.observability import observability
from app.utils.compression import compress_icd_vector_db_response


@tool
def ICD_Vector_Search_Tool(query_texts: List[str]) -> str:
    """
    Searches the ICD-10 vector database for relevant diagnostic codes.
    
    Args:
        query_texts: List of diagnostic terms to search for
        
    Returns:
        Formatted string with search results for each term
    """
    langfuse = observability.get_langfuse()
    
    with langfuse.start_as_current_span(
        name="ICD Vector Search Tool",
    ) as span:
        queries_results = []
        
        for query_text in query_texts:
            if not isinstance(query_text, str):
                raise ValueError("ICD vector search accepts a single query string only.")
            
            # Generate embedding
            embedding = vector_db.get_embedding(query_text)
            
            # Query Pinecone
            results = vector_db.icd_index.query(
                vector=embedding,
                top_k=5,
                include_metadata=True
            )
            
            # Compress and encode results
            results = compress_icd_vector_db_response(results)
            results = encode(results)
            
            queries_results.append(
                f"Results for diagnostic term '{query_text}':\n{results}"
            )
        
        span.update(
            input=query_texts,
            output=queries_results,
            metadata={"index": "ICD-10-CM"}
        )
        
        return "\n\n".join(queries_results)
