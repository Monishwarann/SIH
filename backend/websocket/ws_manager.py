import asyncio
import json
import logging
from typing import List
from fastapi import WebSocket

logger = logging.getLogger("ASTRA-HAR.WebSocketManager")

class WebSocketManager:
    """Multi-channel WebSocket manager handling real-time streaming state updates to React GUI."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Disconnect WebSocket client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Remaining clients: {len(self.active_connections)}")

    async def broadcast_state(self, state_dict: dict):
        """Broadcast state dict to all connected WebSocket clients."""
        if not self.active_connections:
            return

        payload = json.dumps({
            "type": "STATE_UPDATE",
            "timestamp": state_dict.get("timestamp"),
            "data": state_dict
        })

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception as e:
                logger.warning(f"Error sending message to WebSocket client: {e}")
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_event(self, event_type: str, event_data: dict):
        """Broadcast distinct event notification."""
        if not self.active_connections:
            return

        payload = json.dumps({
            "type": "EVENT_NOTIFICATION",
            "event_type": event_type,
            "data": event_data
        })

        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                pass

# Global WebSocket manager instance
ws_manager = WebSocketManager()
