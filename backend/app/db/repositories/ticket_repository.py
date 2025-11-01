from sqlalchemy.orm import Session
from backend.app.db.schemas.event import Ticket
from typing import List, Optional


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Ticket:
        ticket = Ticket(**data)
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def update_status(self, ticket_id: int, status: str) -> Optional[Ticket]:
        ticket = self.get_by_id(ticket_id)
        if ticket:
            ticket.status = status
            self.db.commit()
            self.db.refresh(ticket)
        return ticket

    def list_user_tickets(self, user_id: int) -> List[Ticket]:
        return self.db.query(Ticket).filter(Ticket.user_id == user_id).all()
