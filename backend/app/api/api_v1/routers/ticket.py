from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.ticket import TicketCreate, TicketOut
from app.db.services.ticket_service import TicketService

router = APIRouter()


@router.post("/tickets", response_model=TicketOut)
def reserve_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = TicketService(db).reserve_ticket(payload.model_dump())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": 201,
            "message": "Ticket reserved successfully",
            "data": ticket.model_dump(mode="json"),
        },
    )


@router.post("/tickets/{ticket_id}/pay", response_model=TicketOut)
def pay_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = TicketService(db).mark_as_paid(ticket_id)
    if not ticket:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": 404,
                "message": "Ticket not found",
                "data": None,
            },
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "Ticket paid successfully",
            "data": ticket.model_dump(mode="json"),
        },
    )


@router.get("/tickets/user/{user_id}", response_model=list[TicketOut])
def list_user_tickets(user_id: int, db: Session = Depends(get_db)):
    tickets = TicketService(db).list_user_tickets(user_id)
    tickets_json = [t.model_dump(mode="json") for t in tickets]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "User tickets retrieved successfully",
            "data": tickets_json,
        },
    )
