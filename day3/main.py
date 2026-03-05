from fastapi import FastAPI, HTTPException, status, Body
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str | None = None


books_db: dict[int, Book] = {}


def get_next_book_id() -> int:
    if not books_db:
        return 1
    return max(books_db) + 1


# Index
@app.get("/")
async def index():
    return {"message": "Welcome to BookDB"}


# Add book
@app.post("/books")
async def create_book(book: Book = Body()) -> dict[int, Book]:
    book_id = get_next_book_id()
    books_db[book_id] = book
    return {book_id: book}


# All books
@app.get("/books")
async def get_books() -> dict[int, Book]:
    return books_db


# One book
@app.get("/books/{book_id}")
async def get_book(book_id: int) -> Book:
    try:
        return books_db[book_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )


# Update book
@app.put("/books/{book_id}")
async def update_book(book_id: int, book: Book) -> Book:
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    # books_db[book_id] = book
    book = book.model_dump(exclude_unset=True)
    for k, v in book.items():
        setattr(books_db[book_id], k, v)
    return books_db[book_id]


# Delete book
@app.delete("/books/{book_id}")
async def remove_book(book_id: int) -> dict[str, str]:
    try:
        # books_db.pop(book_id)
        del books_db[book_id]
        return {"message": "Book deleted successfully"}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
