import os
from dotenv import load_dotenv
from typing import List
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import Product, ProductData

load_dotenv()

engine = create_async_engine(os.getenv("DB_URL_ASYNCPG"))

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


"""Data access layer"""


async def insert_product(product: ProductData) -> Product:
    async with Session() as session:
        try:
            stmt = insert(Product).values(
                **product.model_dump(exclude_unset=True, exclude_none=True)).returning(Product)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except Exception as err:
            await session.rollback()
            raise err


async def update_product(product: ProductData) -> Product:
    async with Session() as session:
        try:
            stmt = update(Product).values(
                **product.model_dump(exclude_unset=True, exclude_none=True)).returning(Product)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except Exception as err:
            await session.rollback()
            raise err


async def select_one(id: int) -> Product:
    async with Session() as session:
        try:
            stmt = select(Product).where(Product.id == id)
            result = await session.scalar(stmt)
            return result
        except Exception as err:
            await session.rollback()
            raise err


async def select_all() -> List[Product]:
    async with Session() as session:
        try:
            stmt = select(Product)
            result = await session.scalars(stmt)
            return result.unique().all()
        except Exception as err:
            await session.rollback()
            raise err


async def delete_product(id: int) -> None:
    async with Session() as session:
        try:
            stmt = delete(Product).where(id=id)
            await session.scalar(stmt)
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err


async def pagination(offset: int, limit: int) -> list[Product]:
    async with Session() as session:
        try:
            stmt = select(Product).offset(offset).limit(limit)
            result = await session.scalars(stmt)
            return result.unique().all()
        except Exception as err:
            await session.rollback()
            raise err
