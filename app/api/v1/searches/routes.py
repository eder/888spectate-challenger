from fastapi import APIRouter, Depends, HTTPException
from schemas import SearchModel

search_router = APIRouter()


@search_router.post("/search/")
async def perform_search(
    search_criteria: SearchModel, service: SearchService = Depends()
):
    results = await service.search(search_criteria)
    if not results:
        raise HTTPException(
            status_code=404, detail="No items found based on the search criteria."
        )
    return results
