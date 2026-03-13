from typing import Annotated
from fastapi import Depends, APIRouter, status, Request, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from schemas import UserResponse, TodoRequest, TodoResponse, TodoUpdate
from models import Todos as TodoModel

from routes.auth import login_user, db_dependency

# Пользователь, который прошел аутентификацию и может создавать задачи.
user_dependency = Annotated[UserResponse, Depends(login_user)]

router = APIRouter()


@router.post(
    "/",
    response_model=TodoResponse,
    dependencies=[Depends(login_user)],
)
async def create_todo(
    todo: TodoRequest,
    session: db_dependency,
):
    """Add todo"""
    new_todo = TodoModel(**todo.model_dump(exclude_unset=True))
    new_todo.owner_id = (await login_user(session, Request)).id
    session.add(new_todo)
    await session.commit()
    return new_todo


@router.get(
    "/",
    response_model=list[TodoResponse],
    dependencies=[Depends(login_user)],
)
async def get_todos(
    session: db_dependency,
):
    """All todos"""
    stmt = select(TodoModel)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    dependencies=[Depends(login_user)],
)
async def get_todo(
    todo_id: int,
    session: db_dependency,
):
    """One todo"""
    try:
        return await session.get_one(TodoModel, todo_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    dependencies=[Depends(login_user)],
)
async def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: db_dependency,
):
    """Update todo"""
    try:
        todo_dict = todo.model_dump(exclude_unset=True)
        stmt = update(TodoModel).where(TodoModel.id == todo_id).values(**todo_dict)
        await session.execute(stmt)
        await session.commit()
        return await session.get_one(TodoModel, todo_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )


@router.delete(
    "/{todo_id}",
    dependencies=[Depends(login_user)],
)
async def remove_todo(
    todo_id: int,
    session: db_dependency,
) -> dict[str, str]:
    """Delete todo"""
    try:
        todo_db = await session.get_one(TodoModel, todo_id)
        await session.delete(todo_db)
        await session.commit()
        return {"message": "Todo deleted successfully"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
