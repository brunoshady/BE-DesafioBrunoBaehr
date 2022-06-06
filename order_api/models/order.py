from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, func

from database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    item_description = Column(String, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    item_price = Column(Numeric, nullable=False)
    total_value = Column(Numeric, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_description': self.item_description,
            'item_quantity': str(self.item_quantity),
            'item_price': str(self.item_price),
            'total_value': str(self.total_value),
            'created_at': (str(self.created_at) if self.created_at else self.created_at),
            'updated_at': (str(self.updated_at) if self.updated_at else self.updated_at),
        }

    def __repr__(self):
        return f"Order(id={self.id}, " \
               f"user_id={self.user_id}, " \
               f"item_description={self.item_description}, " \
               f"created_at={str(self.created_at)}, " \
               f"updated_at={str(self.updated_at)})"
