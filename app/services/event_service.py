from repositories.event_repository import EventRepository

class EventService:

    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, event):
        return await self.repository.create(event)
