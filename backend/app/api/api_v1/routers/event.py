from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db

from app.db.schemas.event import EventCreate, Event, EventOut
from app.db.services.event_service import EventService


router = APIRouter()


@router.post("/events", response_model=Event)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = EventService(db).create_event(payload.model_dump())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": 201,
            "message": "Event created successfully",
            "data": event.model_dump(mode="json"),
        },
    )


@router.get("/events", response_model=List[Event])
def list_events(db: Session = Depends(get_db)):
    events = EventService(db).list_events()
    events_out = [EventOut.from_orm(e) for e in events]
    events_json = [e.model_dump(mode="json") for e in events_out]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "All events",
            "data": events_json,
        },
    )


@router.get("/for-you")
def events_for_you(
    user_lat: float = Query(..., description="User latitude"),
    user_lon: float = Query(..., description="User longitude"),
    db: Session = Depends(get_db),
):
    events = EventService(db).get_nearby_events(user_lat, user_lon)
    events_json = [e.model_dump(mode="json") for e in events]

    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Events near you",
            "data": events_json,
        },
    )
