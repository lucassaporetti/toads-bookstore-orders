from pydantic import BaseModel
from typing import Optional
import uuid


class BookOrderData(BaseModel):
    order_id: Optional[uuid.UUID]
    book_id: str
    user_id: str
    quantity: int
    order_date_time: Optional[str]
    order_status: Optional[str]
    delivery_address: Optional[str]
    payment_method: Optional[str]
    total_amount: Optional[float]
    order_notes: Optional[str]
    major_category: Optional[str]
    minor_category: Optional[str]
