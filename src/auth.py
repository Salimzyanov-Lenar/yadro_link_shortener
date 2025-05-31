from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.services import verify_user


security = HTTPBasic()


async def verify_credentials(
        credentials: HTTPBasicCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
):

    username = credentials.username
    password = credentials.password

    is_valid = await verify_user(db, username, password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

    return username
