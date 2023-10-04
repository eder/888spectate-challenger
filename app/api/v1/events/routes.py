
from fastapi import APIRouter, Depends
from utils.dependencies import get_event_service
from schemas import EventBase
from services.event_service import EventService

events_router = APIRouter()

@events_router.get("/events/")
async def get_all_events(service: EventService = Depends(get_event_service)):
    return await service.get_all()

@events_router.post("/events/")
async def create_event(event: EventBase, service: EventService = Depends(get_event_service)):
    return await service.create(event.dict())

