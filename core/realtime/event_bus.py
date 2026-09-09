import asyncio
import logging
from typing import Callable, Dict, List, Any
from core.realtime.event_types import EventType

logger = logging.getLogger("ASTRA-HAR.EventBus")

class EventBus:
    """Async event bus for real-time pub/sub across ASTRA-HAR components."""

    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[Dict[str, Any]], None]]] = {}
        self._global_subscribers: List[Callable[[EventType, Dict[str, Any]], None]] = []

    def subscribe(self, event_type: EventType, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback: Callable[[EventType, Dict[str, Any]], None]):
        """Subscribe to all events across the system."""
        self._global_subscribers.append(callback)

    def publish(self, event_type: EventType, data: Dict[str, Any]):
        """Publish an event to all registered subscribers."""
        # Notify event-specific subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in subscriber for {event_type}: {e}")

        # Notify global subscribers
        for global_cb in self._global_subscribers:
            try:
                global_cb(event_type, data)
            except Exception as e:
                logger.error(f"Error in global subscriber for {event_type}: {e}")

# Global singleton event bus
event_bus = EventBus()
