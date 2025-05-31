import string
import random

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.link_shortener.models import Link
from src.link_shortener.schemas import LinkCreate


def generate_short_code(length=10):
    """
    Функция для генерации короткого кода, который добавится к ссылке
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


async def create_short_link(link_data: LinkCreate, db: AsyncSession) -> Link:
    short_code = generate_short_code()

    while True:
        result = await db.execute(select(Link).filter_by(short_url=short_code))
        existing = result.scalar_one_or_none()
        if not existing:
            break
        short_code = generate_short_code()

    expire_at = datetime.utcnow() + timedelta(days=link_data.expire_in_days or 1)

    new_link = Link(
        original_url=str(link_data.original_url),
        short_url=short_code,
        expire_at=expire_at,
    )

    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)

    return new_link


async def get_original_url(short_code: str, db: AsyncSession) -> Link:
    """
    С помощью short_code достает оригиналькую ссылку из бд
    """
    result = await db.execute(select(Link).filter_by(short_url=short_code))
    link = result.scalar_one_or_none()

    if (not link) or (not link.is_active) or (link.expire_at < datetime.utcnow()):
        link.is_active = False
        return None

    link.redirect_count += 1
    await db.commit()

    return link
