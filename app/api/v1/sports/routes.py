from fastapi import APIRouter, Depends
from schemas import SportBase, SportUpdate, SearchNameModel
from services.sport_service import SportService
from utils.dependencies import get_sport_service


sports_router = APIRouter()


@sports_router.get("/sports/")
async def get_all_sports(service: SportService = Depends(get_sport_service)):
    return await service.get_all()


@sports_router.post("/sports/")
async def create_sport(
    sport: SportBase, service: SportService = Depends(get_sport_service)
):
    return await service.create(sport)


@sports_router.put("/sports/{sport_id}")
async def updating_sport(
    sport_id: int,
    sport: SportUpdate,
    service: SportService = Depends(get_sport_service),
):
    updated_sport = await service.update(sport_id, sport.dict())
    if not updating_sport:
        raise HTTPException(status_code=404, detail="Sport not found")
    return updated_sport


@sports_router.post("/sports/search/")
async def search_sports(
    criteria: SearchNameModel, service: SportService = Depends(get_sport_service)
):
    return await service.search_sports(criteria)


@sports_router.get("/sports/events")
async def filter_sports(service: SportService = Depends(get_sport_service)):
    return await service.filter_sports()
