"""
events_router module.

This module provides a set of API endpoints related to events management.
It allows you to create, retrieve, and update events as well as searching for specific events.

Dependencies:
    - FastAPI
    - EventService
    - Various schema models for data validation and serialization
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas import EventBase, EventUpdate, SearchModel, SearchNameModel
from utils.dependencies import get_event_service
from services.event_service import EventService

events_router = APIRouter()

@events_router.get("/events/")
async def get_all_events(service: EventService = Depends(get_event_service)):
    """
    Retrieve a list of all events.

    Returns:
        list: A list containing all events.
    """
    return await service.get_all()

@events_router.post("/events/")
async def create_event(
    event: EventBase, service: EventService = Depends(get_event_service)
):
    """
    Create a new event.

    Args:
        event (EventBase): The event data.

    Returns:
        dict: The created event data.
    """
    return await service.create(event.dict())

@events_router.put("/events/{event_id}")
async def update_event(
    event_id: int,
    event: EventUpdate,
    service: EventService = Depends(get_event_service),
):
    """
    Update an existing event.

    Args:
        event_id (int): The ID of the event to update.
        event (EventUpdate): The new event data.

    Returns:
        dict: The updated event data.
    """
    updated_event = await service.update(event_id, event.dict())
    return updated_event

@events_router.post("/events/search/")
async def search_events(
    criteria: SearchNameModel, service: EventService = Depends(get_event_service)
):
    """
    Search for events based on given criteria.

    Args:
        criteria (SearchNameModel): The search criteria.

    Returns:
        list: A list of events matching the search criteria.
    """
    return await service.search_events(criteria)

@events_router.get("/events/selections")
async def get_events_selectitons(service: EventService = Depends(get_event_service)):
    """
    Retrieve a list of events' selections.

    Returns:
        list: A list of events' selections.
    """
    return await service.get_events_selectitons()

