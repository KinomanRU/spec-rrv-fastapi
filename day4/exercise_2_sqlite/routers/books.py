from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from schemas import BookSchema, BookSelSchema, BookUpdSchema
from models import BookModel
from db import get_session

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookSelSchema)
async def create_book(
    book: BookSchema,
    session: AsyncSession = Depends(get_session),
):
    """Add book"""
    new_book = BookModel(**book.model_dump(exclude_unset=True))
    session.add(new_book)
    await session.commit()
    return new_book


@router.get("/", response_model=list[BookSelSchema])
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    """All books"""
    # return await session.query(BookModel).all()
    stmt = select(BookModel)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{book_id}", response_model=BookSelSchema)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_session),
):
    """One book"""
    try:
        book = await session.get_one(BookModel, book_id)
        return book
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )


@router.put("/{book_id}", response_model=BookSelSchema)
async def update_book(
    book_id: int,
    book: BookUpdSchema,
    session: AsyncSession = Depends(get_session),
):
    """Update book"""
    try:
        book = book.model_dump(exclude_unset=True)
        # Так проще, но сделал через UPDATE
        # book_db = await session.get_one(BookModel, book_id)
        # for k, v in book.items():
        #     setattr(book_db, k, v)
        # await session.commit()
        stmt = update(BookModel).where(BookModel.id == book_id).values(**book)
        await session.execute(stmt)
        await session.commit()
        book_db = await session.get_one(BookModel, book_id)
        return book_db
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )


@router.delete("/{book_id}")
async def remove_book(
    book_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """Delete book"""
    try:
        book_db = await session.get_one(BookModel, book_id)
        await session.delete(book_db)
        await session.commit()
        return {"message": "Book deleted successfully"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
