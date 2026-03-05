from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str | None = None


class BookGetSchema(BookSchema):
    id: int
