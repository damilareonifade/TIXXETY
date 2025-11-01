from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Event
from app.db.schemas.event import EventOut


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Event:
        event = Event(**data)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return EventOut.from_orm(event)

    def list_all(self) -> List[Event]:
        events = self.db.query(Event).all()
        return [EventOut.from_orm(e) for e in events]

    def get_by_id(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def update_tickets_sold(self, event_id: int):
        event = self.get_by_id(event_id)
        if event:
            event.tickets_sold += 1
            self.db.commit()
            self.db.refresh(event)
        return event
