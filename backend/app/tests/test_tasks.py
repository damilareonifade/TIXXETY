from app import tasks
from app.tasks import expire_unpaid_tickets_task
from app.db.models import TicketStatus, Ticket


def test_example_task():
    task_output = tasks.example_task("Hello World")
    assert task_output == "test task returns Hello World"


def test_expire_unpaid_tickets(test_db):
    """
    Test that unpaid tickets are expired after 2 minutes.
    """
    # Create a reserved ticket
    ticket = (
        test_db.query(Ticket)
        .filter(Ticket.status == TicketStatus.RESERVED)
        .first()
    )
    assert ticket is not None

    # Run the Celery task
    expire_unpaid_tickets_task()

    # Check that the ticket status is updated to expired
    ticket = test_db.query(Ticket).filter(Ticket.id == ticket.id).first()
    assert ticket.status == TicketStatus.EXPIRED
