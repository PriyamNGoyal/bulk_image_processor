from sqlalchemy import Column, String, JSON
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    request_id = Column(String, index=True)
    product_name = Column(String, nullable=False)
    original_urls = Column(JSON, nullable=False)
    compressed_urls = Column(JSON, default=[])
    status = Column(String, default="processing")
