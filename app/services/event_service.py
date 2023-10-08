from datetime import datetime
from schemas import EventType, EventStatus, SearchFilter
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert
import logging


class EventService:
    """
    Service class for managing events.
    """

    def __init__(self, event_repository: EventRepository, logger: logging.Logger):
        """
        Initialize the EventService.

        Args:
            event_repository (EventRepository): The repository for event data.
            logger (logging.Logger): The logger instance for logging events and errors.
        """
        self.event_repository = event_repository
        self.logger = logger

    async def get_all(self):
        """
        Retrieve all events from the database.

        Returns:
            list: List of all events.

        Raises:
            Exception: If there's an error fetching events from the database.
        """
        try:
            return await self.event_repository.get_all()
        except Exception as e:
            self.logger.error(f"Error fetching all events: {e}")
            raise

    async def create(self, event):
        """
        Create a new event based on provided details.

        Args:
            event (dict): Dictionary containing event details.

        Returns:
            dict: The created event's data.

        Raises:
            Exception: If there's an error creating a new event.
        """
        try:
            scheduled_start = datetime.fromisoformat(
                event["scheduled_start"].isoformat()
            )
            actual_start = datetime.fromisoformat(event["actual_start"].isoformat())
            type_value = (
                event["type"].value
                if isinstance(event["type"], EventType)
                else event["type"]
            )
            status_value = (
                event["status"].value
                if isinstance(event["status"], EventStatus)
                else event["status"]
            )
            event_data = {
                "name": event["name"],
                "slug": event["slug"],
                "active": event["active"],
                "type": type_value,
                "sport_id": event["sport_id"],
                "status": status_value,
                "scheduled_start": scheduled_start,
                "actual_start": actual_start,
            }
            return await self.event_repository.create(event_data)
        except Exception as e:
            self.logger.error(f"Error creating event: {e}")
            raise

    async def update(self, event_id: int, event_data: dict) -> dict:
        """
        Update an event based on the given event_id.

        Args:
            event_id (int): ID of the event to be updated.
            event_data (dict): Updated event data.

        Returns:
            dict: The updated event's data.

        Raises:
            Exception: If there's an error updating the event.
        """
        try:
            if event_data["status"].value == "started":
                event_data["actual_start"] = datetime.utcnow()

            def process_field(field, value):
                if (field in ["scheduled_start", "actual_start"]) and isinstance(
                    value, str
                ):
                    return datetime.fromisoformat(value)
                if field == "type" and isinstance(value, EventType):
                    return value.value
                if field == "status" and isinstance(value, EventStatus):
                    return value.value
                return value

            processed_event = {
                key: process_field(key, value)
                for key, value in event_data.items()
                if value is not None
            }
            return_event = prepare_data_for_insert(processed_event)
            return await self.event_repository.update(event_id, return_event)
        except Exception as e:
            self.logger.error(f"Error updating event {event_id}: {e}")
            raise

    async def get_events_selections(self) -> dict:
        """
        Retrieve selections related to events.

        Returns:
            dict: Event selections.

        Raises:
            Exception: If there's an error fetching event selections.
        """
        try:
            return await self.event_repository.get_events_selections()
        except Exception as e:
            self.logger.error(f"Error fetching events' selections: {e}")
            raise

    async def filter_events(self, criteria: dict) -> dict:
        try:
            return await self.event_repository.search_events_with_regex(criteria)
        except Exception as e:
            self.logger.error(f"Error searching for events: {e}")
            raise
