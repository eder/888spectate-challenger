"""
events_router module.

This module provides a set of API endpoints related to events management.
It allows you to create, retrieve, and update events as well as searching for specific events.

Dependencies:
    - FastAPI
    - EventService
    - Various schema models for data validation and serialization
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from schemas import EventBase, EventUpdate, EventFilter
from utils.dependencies import get_event_service, get_logger
from services.event_service import EventService

events_router = APIRouter()


@events_router.get("/events/")
async def get_all_events(
    service: EventService = Depends(get_event_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Fetching all events...")
        return await service.get_all()
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching events."
        )


@events_router.post("/events/")
async def create_event(
    event: EventBase,
    service: EventService = Depends(get_event_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Creating a new event...")
        return await service.create(event.dict())
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error creating event."
        )


@events_router.put("/events/{event_id}")
async def update_event(
    event_id: int,
    event: EventUpdate,
    service: EventService = Depends(get_event_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info(f"Updating event with ID {event_id}...")
        updated_event = await service.update(event_id, event.dict())
        return updated_event
    except Exception as e:
        logger.error(f"Error updating event {event_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error updating event {event_id}."
        )


@events_router.post("/events/search/")
async def filter_events(
    criteria: EventFilter,
    service: EventService = Depends(get_event_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Searching for events based on given criteria...")
        return await service.filter_events(criteria.dict())
    except Exception as e:
        logger.error(f"Error searching for events: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error searching for events."
        )


@events_router.get("/events/selections")
async def get_events_selections(
    service: EventService = Depends(get_event_service),
    logger: logging.Logger = Depends(get_logger),
):
    try:
        logger.info("Fetching events' selections...")
        return await service.get_events_selections()
    except Exception as e:
        logger.error(f"Error fetching events' selections: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching events' selections."
        )
