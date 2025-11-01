from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.db.schemas.event import EventInDB
from app.db.models import TicketStatus


class TicketBase(BaseModel):
    status: Optional[str] = "reserved"


class TicketCreate(TicketBase):
    user_id: int
    event_id: int


class TicketUpdate(BaseModel):
    status: Optional[str] = None


class TicketOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: TicketStatus
    created_at: datetime

    model_config = {
        "from_attributes": True  # allows from_orm usage in Pydantic v2
    }


class TicketInDBBase(TicketBase):
    id: int
    user_id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Ticket(TicketInDBBase):
    event: Optional[EventInDB] = None


class TicketInDB(TicketInDBBase):
    pass
