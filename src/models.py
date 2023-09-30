from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ARRAY, Boolean, Numeric
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# Database Models
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    brand_name = Column(String)
    current_price = Column(Numeric(precision=8, scale=2))
    previous_price = Column(Numeric(precision=8, scale=2))
    discount_percent = Column(Integer)
    currency = Column(String)
    url = Column(String)
    images = Column(ARRAY(String))
    product_code = Column(Integer)
    selling_fast = Column(Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Serializer Schemas
class ProductData(BaseModel):
    id: int
    name: str
    brand_name: str
    current_price: float
    previous_price: Optional[float]
    discount_percent: Optional[int] = None
    currency: str
    url: str
    images: List[str]
    product_code: int
    selling_fast: bool

    class Config:
        from_attributes = True
