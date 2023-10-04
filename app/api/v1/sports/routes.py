from fastapi import APIRouter, Depends

from utils.dependencies import get_sport_service
from services.sport_service import SportService
from schemas import SportBase

sports_router = APIRouter()

@sports_router.get("/sports/")
async def get_all_sports(service: SportService = Depends(get_sport_service)):
    return await service.get_all()

@sports_router.post("/sports/")
async def create_sport(sport: SportBase, service: SportService = Depends(get_sport_service)):
    return await service.create(sport)

