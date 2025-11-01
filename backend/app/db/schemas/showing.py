from pydantic import BaseModel
from datetime import datetime
from .book import Book
import typing as t


class ShowingBase(BaseModel):
    title: str
    start: datetime
    end: datetime

    class Config:
        from_attributes = True


class ShowingOut(ShowingBase):
    pass


class ShowingCreate(ShowingBase):
    pass


class ShowingEdit(ShowingBase):
    number: t.Optional[int] = None

    class Config:
        from_attribute = True


class Showing(ShowingBase):
    id: int
    hall_id: int
    movie_id: int
    is_active: bool
    books: t.List[Book] = None

    class Config:
        from_attributes = True
