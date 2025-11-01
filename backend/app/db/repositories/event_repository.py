from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Event
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import func
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

    def nearby_events(
        self, user_lat: float, user_lon: float, radius_km: float = 10
    ):
        user_point = from_shape(Point(user_lon, user_lat), srid=4326)
        radius_m = radius_km * 1000  # meters

        return (
            self.db.query(Event)
            .filter(func.ST_DWithin(Event.location, user_point, radius_m))
            .all()
        )
