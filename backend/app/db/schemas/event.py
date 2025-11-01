from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    total_tickets: int
    tickets_sold: int = 0
    venue: str


class EventCreate(EventBase):
    pass


class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    total_tickets: int
    tickets_sold: int
    venue: str

    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_tickets: Optional[int] = None
    tickets_sold: Optional[int] = None
    venue: Optional[str] = None


class EventInDBBase(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# forward declaration to avoid circular import
class TicketSummary(BaseModel):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class Event(EventInDBBase):
    tickets: Optional[List[TicketSummary]] = []


class EventInDB(EventInDBBase):
    pass
