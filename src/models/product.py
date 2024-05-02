from datetime import datetime
import decimal
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import ARRAY, TIMESTAMP, Numeric, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


# Database Models
class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    slug: Mapped[str] = mapped_column(unique=True)
    brand_name: Mapped[str]
    current_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(precision=8, scale=2)
    )
    previous_price: Mapped[Optional[decimal.Decimal]] = mapped_column(
        Numeric(precision=8, scale=2)
    )
    discount_percent: Mapped[int]
    currency: Mapped[str]
    url: Mapped[str]
    images: Mapped[list[str]] = mapped_column(ARRAY(String))
    product_code: Mapped[int]
    selling_fast: Mapped[bool]
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    async def find(cls, db_session: AsyncSession, slug: str):
        """
        Find a product in the database by its slug.

        Args:
            db_session (AsyncSession): The database session to use for the query.
            slug (str): The slug of the product to find.

        Returns:
            ProductOrm: The found product object.

        Raises:
            HTTPException: If no product is found with the given slug.
        """
        stmt = select(cls).where(cls.slug == slug)
        result = await db_session.execute(stmt)
        product = result.scalars().first()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "Product not found": f"There is no product for requested slug value : {slug}"
                },
            )
        else:
            return product
