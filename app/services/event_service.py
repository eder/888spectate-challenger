from datetime import datetime

from schemas import EventType, EventStatus, SearchFilter
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert
class EventService:

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def get_all(self):
        return await self.event_repository.get_all()

    async def create(self, event):
        scheduled_start = datetime.fromisoformat(event["scheduled_start"].isoformat())
        actual_start = datetime.fromisoformat(event["actual_start"].isoformat())
        type_value = event["type"].value if isinstance(event["type"], EventType) else event["type"]
        status_value = event["status"].value if isinstance(event["status"], EventStatus) else event["status"]
        event_data = {
            "name": event["name"],
            "slug": event["slug"],
            "active":event["active"],
            "type": type_value,
            "sport_id": event["sport_id"],
            "status": status_value,
            "scheduled_start": scheduled_start,
            "actual_start": actual_start 
        }
        
        return await self.event_repository.create(event_data)

    async def update(self, event_id: int, event_data: dict) -> dict:
            # Actual start (created at the time the event has the status changed to "Started")
            if event_data["status"].value == "started":
                event_data["actual_start"] = datetime.utcnow()

            def process_field(field, value):
                if (field in ["scheduled_start", "actual_start"]) and isinstance(value, str):
                    return datetime.fromisoformat(value)
                if field == "type" and isinstance(value, EventType):
                    return value.value
                if field == "status" and isinstance(value, EventStatus):
                    return value.value
                return value
            
            processed_event = {key: process_field(key, value) for key, value in event_data.items() if value is not None} 
            res = prepare_data_for_insert(processed_event)
            return await self.event_repository.update(event_id, res['original_data']
) 

    async def search_events(self, criteria: SearchFilter):
        if criteria.min_active_selections:
            return await self.event_repository.get_events_with_min_active_selections(criteria.min_active_selections)
        return await self.event_repository.search_events_by_criteria(criteria)
