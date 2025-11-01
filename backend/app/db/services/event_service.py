from fastapi import HTTPException, status
from app.db.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, db):
        self.repo = EventRepository(db)

    def create_event(self, data):
        return self.repo.create(data)

    def list_events(self):
        return self.repo.list_all()

    def get_event(self, event_id: int):
        event = self.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        return event
