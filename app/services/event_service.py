from schemas import SearchFilter
from repositories.event_repository import EventRepository

class EventService:

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def get_all(self):
        return await self.event_repository.get_all()

    async def create(self, event):
        return await self.event_repository.create(event)

    async def update(self, event_id: int, event_data: dict) -> dict:
        return await self.event_repository.update(event_id, event_data)

    async def search_events(self, criteria: SearchFilter):
        return await self.event_repository.search_events_by_criteria(criteria)
    
