from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import verify_credentials
from src.link_shortener.services import create_short_link, get_original_url
from src.link_shortener.schemas import LinkCreate, LinkOut
from src.link_shortener.models import Link


router = APIRouter(prefix='/links', tags=["urls"])


@router.get("/")
async def list_links(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db)
):
    """ Хэндлер для вывода списка всех созданных ссылок """
    result = await db.execute(select(Link).offset(skip).limit(limit))
    links = result.scalars().all()
    return links


@router.get('/deactivate/{short_url}')
async def deactivate_link(
    short_url: str,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_credentials)
):
    """ Хэндлер для деактивации созданной укороченной ссылки """
    result = await db.execute(select(Link).filter_by(short_url=short_url))
    link = result.scalar_one_or_none()
    link.is_active = False

    await db.commit()

    return link


@router.post("/shorten", response_model=LinkOut)
async def shorten_url(
        link_data: LinkCreate,
        db: AsyncSession = Depends(get_db),
        _: str = Depends(verify_credentials),
):
    """ Хэндлер для создания короткой ссылки """
    link = await create_short_link(link_data, db)

    full_link = "http://localhost:8000/links/" + link.short_url
    link.short_url = full_link

    return link


@router.get("/{short_url}")
async def redirect(short_url: str, db: AsyncSession = Depends(get_db)):
    """ Хэндлер для редиректа, принимающий код который был создан для короткой ссылки """
    link = await get_original_url(short_url, db)

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found or expired")

    return RedirectResponse(url=str(link.original_url))
