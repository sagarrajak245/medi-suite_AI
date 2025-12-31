"""
CPT-4 Vector Search Tool
RAG tool for retrieving CPT-4 codes from Pinecone
"""

from typing import List
from crewai.tools import tool
from toon_format import encode
from app.core.vector_db import vector_db
from app.core.observability import observability
from app.utils.compression import compress_vector_db_response


@tool
def CPT_Vector_Search_Tool(query_texts: List[str]) -> str:
    """
    Searches the CPT-4 vector database for relevant procedure codes.
    
    Args:
        query_texts: List of procedure/service terms to search for
        
    Returns:
        Formatted string with search results for each term
    """
    langfuse = observability.get_langfuse()
    
    with langfuse.start_as_current_span(
        name="CPT Vector Search Tool",
    ) as span:
        queries_results = []
        
        for query_text in query_texts:
            if not isinstance(query_text, str):
                raise ValueError("CPT vector search accepts a single query string only.")
            
            # Generate embedding
            embedding = vector_db.get_embedding(query_text)
            
            # Query Pinecone
            results = vector_db.cpt_index.query(
                vector=embedding,
                top_k=5,
                include_metadata=True
            )
            
            # Compress and encode results
            results = compress_vector_db_response(results)
            results = encode(results)
            
            queries_results.append(
                f"Results for procedure term '{query_text}':\n{results}"
            )
        
        span.update(
            input=query_texts,
            output=queries_results,
            metadata={"index": "CPT"}
        )
        
        return "\n\n".join(queries_results)
