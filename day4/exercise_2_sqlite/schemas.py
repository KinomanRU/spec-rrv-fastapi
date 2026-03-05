from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str | None = None


class BookSelSchema(BookSchema):
    id: int


class BookUpdSchema(BookSchema):
    title: str | None = None
