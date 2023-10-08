from fastapi import APIRouter, Depends, HTTPException
from schemas import EventBase, EventUpdate, SearchModel, SearchNameModel
from utils.dependencies import get_event_service
from services.event_service import EventService


events_router = APIRouter()


@events_router.get("/events/")
async def get_all_events(service: EventService = Depends(get_event_service)):
    return await service.get_all()


@events_router.post("/events/")
async def create_event(
    event: EventBase, service: EventService = Depends(get_event_service)
):
    return await service.create(event.dict())


@events_router.put("/events/{event_id}")
async def update_event(
    event_id: int,
    event: EventUpdate,
    service: EventService = Depends(get_event_service),
):
    updated_event = await service.update(event_id, event.dict())
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


@events_router.post("/events/search/")
async def search_events(
    criteria: SearchNameModel, service: EventService = Depends(get_event_service)
):
    return await service.search_events(criteria)
