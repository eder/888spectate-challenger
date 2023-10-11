from datetime import datetime
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert
from utils.slugify import to_slug
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
                "slug": to_slug(event['name']),
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

    async def update(self, event_id: int, event: dict) -> dict:
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
            event['slug'] = to_slug(event['name'])

            if event["status"] == "started":
                event["actual_start"] = datetime.utcnow()
                
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
                for key, value in event.items()
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
            query_parts = [
                "WITH ActiveSelections AS (",
                "    SELECT e.id, e.name, COUNT(s.id) as active_selections_count",
                "    FROM events e",
                "    LEFT JOIN selections s ON e.id = s.event_id AND s.active = TRUE",
                "    WHERE 1=1"
            ]

            params = []

            if "name_regex" in criteria and criteria["name_regex"]:
                query_parts.append("    AND e.name ~ $" + str(len(params) + 1))
                params.append(criteria["name_regex"])

            if "active" in criteria and isinstance(criteria["active"], bool):
                query_parts.append("    AND e.active = $" + str(len(params) + 1))
                params.append(criteria["active"])

            threshold_value = criteria.get("threshold", 1)
            if threshold_value:
                query_parts.append("    GROUP BY e.id, e.name")
                query_parts.append("    HAVING COUNT(s.id) >= $" + str(len(params) + 1))
                params.append(threshold_value)
            else:
                query_parts.append("    GROUP BY e.id, e.name")

            if criteria.get("start_time") and criteria.get("end_time"):
                query_parts.extend([
                    "),",
                    "TimeRangeEvents AS (",
                    "    SELECT * FROM events",
                    f"    WHERE actual_start BETWEEN ${str(len(params) + 1)} AND ${str(len(params) + 2)})",
                ])
                params.extend([criteria["start_time"], criteria["end_time"]])
                query_parts.extend([
                    "SELECT a.id, a.name, COALESCE(a.active_selections_count, 0) as active_selections_count FROM ActiveSelections a",
                    "UNION ALL",
                    "SELECT t.id, t.name, 0 as active_selections_count FROM TimeRangeEvents t",
                    "WHERE NOT EXISTS (SELECT 1 FROM ActiveSelections a WHERE a.id = t.id)"
                ])
            else:
                query_parts.extend([
                    ")",
                    "SELECT a.id, a.name, COALESCE(a.active_selections_count, 0) as active_selections_count FROM ActiveSelections a"
                ])

            query = "\n".join(query_parts)
            print(query)
            return await self.event_repository.filter_events(query, params)
        except Exception as e:
            self.logger.error(f"Error searching for events: {e}")
            raise
