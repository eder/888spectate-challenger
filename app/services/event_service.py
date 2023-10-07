from datetime import datetime

from schemas import EventType, EventStatus, SearchFilter
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert

class EventService:
    """
    Service class for managing events.
    """

    def __init__(self, event_repository: EventRepository):
        """
        Initialize the EventService.

        Args:
            event_repository (EventRepository): The repository for event data.
        """
        self.event_repository = event_repository

    async def get_all(self):
        """
        Get all events.

        Returns:
            list: A list of all events.
        """
        return await self.event_repository.get_all()

    async def create(self, event):
        """
        Create a new event.

        Args:
            event (dict): The event data to create.

        Returns:
            dict: The created event data.
        """
        scheduled_start = datetime.fromisoformat(event["scheduled_start"].isoformat())
        actual_start = datetime.fromisoformat(event["actual_start"].isoformat())
        type_value = event["type"].value if isinstance(event["type"], EventType) else event["type"]
        status_value = event["status"].value if isinstance(event["status"], EventStatus) else event["status"]
        event_data = {
            "name": event["name"],
            "slug": event["slug"],
            "active": event["active"],
            "type": type_value,
            "sport_id": event["sport_id"],
            "status": status_value,
            "scheduled_start": scheduled_start,
            "actual_start": actual_start
        }

        return await self.event_repository.create(event_data)

    async def update(self, event_id: int, event_data: dict) -> dict:
        """
        Update an event.

        Args:
            event_id (int): The ID of the event to update.
            event_data (dict): The updated event data.

        Returns:
            dict: The updated event data.
        """
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
        return_event = prepare_data_for_insert(processed_event)
        return await self.event_repository.update(event_id, return_event)

    async def search_events(self, criteria: SearchFilter):
        """
        Search events based on specified criteria.

        Args:
            criteria (SearchFilter): The search criteria.

        Returns:
            list: A list of events that match the search criteria.
        """
        if criteria.min_active_selections:
            return await self.event_repository.get_events_with_min_active_selections(criteria.min_active_selections)
        return await self.event_repository.search_events_by_criteria(criteria)

