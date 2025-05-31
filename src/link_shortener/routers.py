from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import verify_credentials
from src.link_shortener.services import create_short_link, get_original_url
from src.link_shortener.schemas import LinkCreate, LinkOut


router = APIRouter(prefix='/urls', tags=["urls"])


@router.post("/shorten", response_model=LinkOut)
async def shorten_url(
        link_data: LinkCreate,
        db: AsyncSession = Depends(get_db),
        _: str = Depends(verify_credentials),
):
    """
    API для создания короткой ссылки
    """
    link = await create_short_link(link_data, db)

    # Заменить localhost на требуемый ip
    full_link = "http://localhost:8000/urls/" + link.short_url
    link.short_url = full_link

    return link


@router.get("/{short_code}")
async def redirect(
        short_code: str,
        db: AsyncSession = Depends(get_db),
):
    """
    API которое делает редирект на оригинальную ссылку
    """
    link = await get_original_url(short_code, db)

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found or expired")

    return RedirectResponse(url=str(link.original_url))
