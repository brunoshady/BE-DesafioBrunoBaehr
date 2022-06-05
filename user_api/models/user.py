from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cpf': self.cpf,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': (str(self.created_at) if self.created_at else self.created_at),
            'updated_at': (str(self.updated_at) if self.updated_at else self.updated_at),
        }

    def __repr__(self):
        return f"User(id={self.id}, " \
               f"name={self.name}, " \
               f"cpf={self.cpf}, " \
               f"email={self.email}, " \
               f"phone_number={self.phone_number}, " \
               f"created_at={str(self.created_at)}, " \
               f"updated_at={str(self.updated_at)})"
