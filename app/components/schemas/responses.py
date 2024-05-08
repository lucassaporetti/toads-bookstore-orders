from pydantic import BaseModel
from typing import Optional
import uuid


class BookOrderData(BaseModel):
    order_id: str = str(uuid.uuid4())
    book_id: str
    user_id: str
    quantity: int
    order_date_time: Optional[str] = None
    order_status: Optional[str] = None
    delivery_address: Optional[str] = None
    payment_method: Optional[str] = None
    total_amount: Optional[float] = None
    order_notes: Optional[str] = None
    major_category: Optional[str] = None
    minor_category: Optional[str] = None
