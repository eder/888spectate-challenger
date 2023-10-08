"""
sports_router module.

This module provides a set of API endpoints related to sports management.
It allows you to create, retrieve, update, and search sports, as well as fetching associated events.

Dependencies:
    - FastAPI
    - SportService
    - Schema models for data validation and serialization
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from schemas import SportBase, SportUpdate, SearchNameModel, SportFilter
from services.sport_service import SportService
from utils.dependencies import get_sport_service, get_logger

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
        return await service.create(sport)
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


@sports_router.post("/sports/search/")
async def search_sports(
    criteria: SportFilter,
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Searching for sports based on given criteria...")
        return await service.search_sports(criteria.dict())
    except Exception as e:
        logger.error(f"Error searching for sports: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error searching for sports."
        )


@sports_router.get("/sports/events")
async def get_sports_events(
    service: SportService = Depends(get_sport_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Fetching sports' events...")
        return await service.get_sports_events()
    except Exception as e:
        logger.error(f"Error fetching sports' events: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching sports' events."
        )
