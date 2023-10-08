"""
selections_router module.

This module provides a set of API endpoints related to selections management.
It allows you to create, retrieve, update, and search for specific selections.

Dependencies:
    - FastAPI
    - SelectionService
    - Various schema models for data validation and serialization
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from schemas import SelectionBase, SelectionUpdate, SearchNameModel
from services.selection_service import SelectionService
from utils.custom_exceptions import CreationError, ValidationError, ForeignKeyError
from utils.dependencies import get_selection_service, get_logger

selections_router = APIRouter()


@selections_router.get("/selections/")
async def get_all_selections(
    service: SelectionService = Depends(get_selection_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Fetching all selections...")
        return await service.get_all()
    except Exception as e:
        logger.error(f"Error fetching selections: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching selections."
        )


@selections_router.post("/selections/")
async def create_selection(
    selection: SelectionBase,
    service: SelectionService = Depends(get_selection_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Creating a new selection...")
        return await service.create(selection.dict())
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except CreationError as ce:
        logger.error(f"Creation error: {ce}")
        raise HTTPException(status_code=400, detail=str(ce))
    except Exception as e:
        logger.error(f"Error creating selection: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error creating selection."
        )


@selections_router.put("/selections/{selection_id}")
async def update_selection(
    selection_id: int,
    selection: SelectionUpdate,
    service: SelectionService = Depends(get_selection_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info(f"Updating selection with ID {selection_id}...")
        updated_selection = await service.update(selection_id, selection.dict())
        if not updated_selection:
            raise ValueError("Updated selection is None or not found")
        return updated_selection
    except ForeignKeyError as fe:
        logger.error(f"Foreign key error: {fe}")
        raise HTTPException(status_code=400, detail=str(fe))
    except Exception as e:
        logger.error(f"Error updating selection {selection_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error updating selection {selection_id}.",
        )


@selections_router.post("/selections/search/")
async def search_selections(
    criteria: SearchNameModel,
    service: SelectionService = Depends(get_selection_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Searching for selections based on given criteria...")
        return await service.search_selections(criteria)
    except Exception as e:
        logger.error(f"Error searching for selections: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error searching for selections."
        )
