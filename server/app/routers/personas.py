"""
Personas API Endpoint
Provides information about available user personas
"""

from fastapi import APIRouter
from typing import Dict
from ..services.personas import list_personas

router = APIRouter(prefix="/personas", tags=["personas"])


@router.get("/list")
async def get_personas() -> Dict[str, Dict[str, str]]:
    """
    Get list of available user personas with metadata
    
    Returns:
        Dictionary of personas with name, role, and description
    """
    return list_personas()
