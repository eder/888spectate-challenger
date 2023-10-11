import logging

from fastapi import APIRouter, Depends, HTTPException
from schemas import SportBase, SportUpdate, Filters
from services.sport_service import SportService
from utils.dependencies import get_sport_service, get_logger
from utils.slugify import to_slug


sports_router = APIRouter()


@sports_router.get("/sports/")
async def get_all_sports(
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Fetching all sports...")
        return await service.get_all()
    except Exception as e:
        logger.error(f"Error fetching sports: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching sports."
        )


@sports_router.post("/sports/")
async def create_sport(
    sport: SportBase,
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Creating a new sport...")
        return await service.create(sport.dict())
    except Exception as e:
        logger.error(f"Error creating sport: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error creating sport."
        )


@sports_router.put("/sports/{sport_id}")
async def updating_sport(
    sport_id: int,
    sport: SportUpdate,
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info(f"Updating sport with ID {sport_id}...")
        updated_sport = await service.update(sport_id, sport.dict())
        if not updated_sport:
            raise HTTPException(status_code=404, detail="Sport not found")
        return updated_sport
    except Exception as e:
        logger.error(f"Error updating sport {sport_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error updating sport {sport_id}."
        )


@sports_router.post("/sports/filters/")
async def filter_sports(
    criteria: Filters,
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Filter for sports based on given criteria...")
        return await service.filter_sports(criteria.dict())
    except Exception as e:
        logger.error(f"Error searching for sports: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error searching for sports."
        )

