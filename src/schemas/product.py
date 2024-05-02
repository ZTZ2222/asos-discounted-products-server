from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SProduct(BaseModel):
    id: int
    name: str
    slug: str
    brand_name: str
    current_price: float
    previous_price: Optional[float]
    discount_percent: Optional[int] = None
    currency: str
    url: str
    images: list[str]
    product_code: int
    selling_fast: bool
    updated_at: datetime

    class Config:
        from_attributes = True
