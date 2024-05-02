from datetime import datetime
import decimal
from typing import Optional
from sqlalchemy import ARRAY, TIMESTAMP, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


# Database Models
class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
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
