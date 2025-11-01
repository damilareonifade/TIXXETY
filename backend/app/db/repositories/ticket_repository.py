from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Ticket
from app.db.schemas.ticket import TicketOut


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> TicketOut:
        ticket = Ticket(**data)
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return TicketOut.from_orm(ticket)  # single object

    def get_by_id(self, ticket_id: int) -> Optional[TicketOut]:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        return TicketOut.from_orm(ticket) if ticket else None

    def update_status(self, ticket_id: int, status: str) -> Optional[TicketOut]:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket:
            ticket.status = status
            self.db.commit()
            self.db.refresh(ticket)
            return TicketOut.from_orm(ticket)
        return None

    def list_user_tickets(self, user_id: int) -> List[TicketOut]:
        tickets = self.db.query(Ticket).filter(Ticket.user_id == user_id).all()
        return [
            TicketOut.from_orm(t) for t in tickets
        ]  # list of Pydantic models
