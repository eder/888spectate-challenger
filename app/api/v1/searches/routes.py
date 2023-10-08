from fastapi import APIRouter, Depends, HTTPException
from schemas import SearchModel
from utils.dependencies import get_search_service
from services.search_service import SearchService


searches_router = APIRouter()


@searches_router.post("/searches/")
async def search_events(
    criteria: SearchModel, service: SearchService = Depends(get_search_service)
):
    return await service.search(criteria.dict())
