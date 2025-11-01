from fastapi import HTTPException, status
from app.db.repositories.ticket_repository import TicketRepository
from app.db.repositories.event_repository import EventRepository
from backend.app.db.models import Ticket


class TicketService:
    def __init__(self, db):
        self.repo = TicketRepository(db)
        self.event_repo = EventRepository(db)

    def reserve_ticket(self, data):
        event = self.event_repo.get_by_id(data["event_id"])
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )

        if event.tickets_sold >= event.total_tickets:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tickets sold out",
            )

        ticket = self.repo.create(data)
        self.event_repo.update_tickets_sold(event.id)
        return ticket

    def mark_as_paid(self, ticket_id: int):
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
            )

        if ticket.status == "paid":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket already paid",
            )

        return self.repo.update_status(ticket_id, "paid")

    def expire_unpaid_tickets(self):
        # Called by Celery periodically
        unpaid_tickets = (
            self.repo.db.query(self.repo.db_model)
            .filter(Ticket.status == "reserved")
            .all()
        )
        for ticket in unpaid_tickets:
            self.repo.update_status(ticket.id, "expired")
