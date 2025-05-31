from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from passlib.context import CryptContext

from src.users.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_user(db: AsyncSession, username: str, password: str):

    # Check if user exists
    result = await db.execute(select(User).where(User.username == username))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken",
        )

    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def verify_user(db: AsyncSession, username: str, password: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    return verify_password(password, user.password)
