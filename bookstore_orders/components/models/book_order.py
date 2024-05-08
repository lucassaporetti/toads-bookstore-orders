import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float
)

from bookstore_orders.components.utils.database.service import Base


class BookOrder(Base):
    __tablename__ = 'book_orders'

    order_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    book_id = Column(String)
    user_id = Column(String)
    quantity = Column(Integer)
    order_date_time = Column(DateTime)
    order_status = Column(String)
    delivery_address = Column(String)
    payment_method = Column(String)
    total_amount = Column(Float)
    order_notes = Column(String)
    major_category = Column(String)
    minor_category = Column(String)
