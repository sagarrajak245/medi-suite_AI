"""
Response Compression Utilities
Compress vector database responses for efficient token usage
"""

from typing import Dict, Any, List


def compress_vector_db_response(resp) -> Dict[str, Any]:
    """
    Compress generic vector database response.
    
    Args:
        resp: Pinecone query response
        
    Returns:
        Compact dictionary with essential fields
    """
    compact = {
        "matches": [
            {
                "id": m["id"],
                "desc": m["metadata"].get("description", ""),
                "score": round(m["score"], 4)
            }
            for m in resp.matches
        ]
    }
    return compact


def compress_icd_vector_db_response(resp) -> Dict[str, Any]:
    """
    Compress ICD-10 specific vector database response.
    
    Args:
        resp: Pinecone query response from ICD index
        
    Returns:
        Compact dictionary with ICD-specific fields
    """
    compact = {
        "matches": [
            {
                "id": m["id"],
                "category": m["metadata"].get("category", ""),
                "disease": m["metadata"].get("disease", ""),
                "score": round(m["score"], 4)
            }
            for m in resp.matches
        ]
    }
    return compact
