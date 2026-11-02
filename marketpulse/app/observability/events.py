import time
import uuid
from typing import List, Callable, Optional, Dict, Any
from app.schemas import ExecutionEvent, EventType, utc_now_iso


class ExecutionEventEmitter:
    """
    In-memory and persistent Event Emitter for real-time workflow observability.
    Captures fine-grained events across all multi-agent stages.
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.events: List[ExecutionEvent] = []
        self._listeners: List[Callable[[ExecutionEvent], None]] = []

    def subscribe(self, listener: Callable[[ExecutionEvent], None]):
        """Subscribe a callback to live event emissions."""
        self._listeners.append(listener)

    def emit(
        self,
        event_type: EventType,
        agent_name: str,
        node_name: str,
        message: str,
        status: str = "completed",
        entity_ids: Optional[List[str]] = None,
        duration_ms: Optional[int] = None,
    ) -> ExecutionEvent:
        """Create and emit an execution event to all active subscribers."""
        event = ExecutionEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
            run_id=self.run_id,
            timestamp=utc_now_iso(),
            agent_name=agent_name,
            node_name=node_name,
            event_type=event_type,
            status=status,
            message=message,
            entity_ids=entity_ids or [],
            duration_ms=duration_ms,
        )
        self.events.append(event)

        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass

        return event

    def get_events(self) -> List[ExecutionEvent]:
        return list(self.events)

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [e.model_dump() for e in self.events]
