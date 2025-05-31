from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserCreate
from src.users.services import create_user
from src.database import get_db


router = APIRouter(prefix='/users', tags=["users"])


@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user.username, user.password)
    return {"id": new_user.id, "username": new_user.username}
