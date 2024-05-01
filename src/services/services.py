from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update, delete, insert

from ..schemas.schemas import SProduct
from ..models.models import ProductOrm
from ..database import async_session_factory


async def insert_product(product: SProduct) -> ProductOrm:
    async with async_session_factory() as session:
        try:
            stmt = (
                insert(ProductOrm)
                .values(**product.model_dump(exclude_unset=True, exclude_none=True))
                .returning(ProductOrm)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except Exception as err:
            await session.rollback()
            raise err


async def update_product(product: SProduct) -> ProductOrm:
    async with async_session_factory() as session:
        try:
            stmt = (
                update(ProductOrm)
                .values(**product.model_dump(exclude_unset=True, exclude_none=True))
                .returning(ProductOrm)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except Exception as err:
            await session.rollback()
            raise err


async def select_one(id: int) -> ProductOrm:
    async with async_session_factory() as session:
        try:
            stmt = select(ProductOrm).where(ProductOrm.id == id)
            result = await session.scalar(stmt)
            return result
        except Exception as err:
            await session.rollback()
            raise err


async def select_products(offset: int, limit: int) -> list[ProductOrm]:
    async with async_session_factory() as session:
        try:
            stmt = select(ProductOrm).offset(offset).limit(limit)
            result = await session.scalars(stmt)
            return result.unique().all()
        except Exception as err:
            await session.rollback()
            raise err


async def delete_product(id: int) -> None:
    async with async_session_factory() as session:
        try:
            stmt = delete(ProductOrm).where(id=id)
            await session.scalar(stmt)
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err


async def pagination(offset: int, limit: int) -> list[ProductOrm]:
    async with async_session_factory() as session:
        try:
            stmt = select(ProductOrm).offset(offset).limit(limit)
            result = await session.scalars(stmt)
            return result.unique().all()
        except Exception as err:
            await session.rollback()
            raise err


async def delete_old_products() -> None:
    four_weeks_ago = datetime.now(timezone.utc) - timedelta(weeks=4)

    async with async_session_factory() as session:
        try:
            stmt = delete(ProductOrm).where(ProductOrm.updated_at <= four_weeks_ago)
            await session.execute(stmt)
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err
