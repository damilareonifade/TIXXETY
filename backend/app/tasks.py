from app.core.celery_app import celery_app
from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.db.services.ticket_service import TicketService


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"test task returns {word}"


@celery_app.task(acks_late=True)
def expire_unpaid_tickets_task():
    """
    Celery task to expire unpaid tickets after 2 minutes.
    """
    db = SessionLocal()
    try:
        TicketService(db).expire_unpaid_tickets()
    finally:
        db.close()
