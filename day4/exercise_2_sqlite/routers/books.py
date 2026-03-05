from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import BookSchema, BookGetSchema
from models import BookModel
from db import get_session

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookGetSchema)
async def create_book(book: BookSchema, session: AsyncSession = Depends(get_session)):
    """Add book"""
    new_book = BookModel(**book.dict())
    session.add(new_book)
    await session.commit()
    return new_book


@router.get("/", response_model=list[BookGetSchema])
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    """All books"""
    # return await session.query(BookModel).all()
    stmt = select(BookModel)
    result = await session.execute(stmt)
    return result.scalars().all()


# @router.get("/{book_id}")
# async def get_book(book_id: int) -> Book:
#     """One book"""
#     try:
#         return books_db[book_id]
#     except KeyError:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found",
#         )
#
#
# @router.put("/{book_id}")
# async def update_book(book_id: int, book: Book) -> Book:
#     """Update book"""
#     if book_id not in books_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found",
#         )
#     # books_db[book_id] = book
#     book = book.model_dump(exclude_unset=True)
#     for k, v in book.items():
#         setattr(books_db[book_id], k, v)
#     return books_db[book_id]
#
#
# @router.delete("/{book_id}")
# async def remove_book(book_id: int) -> dict[str, str]:
#     """Delete book"""
#     try:
#         # books_db.pop(book_id)
#         del books_db[book_id]
#         return {"message": "Book deleted successfully"}
#     except KeyError:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found",
#         )
