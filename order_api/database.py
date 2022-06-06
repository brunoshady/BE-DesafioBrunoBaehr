import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = os.environ.get('POSTGRES_URL')

Base = declarative_base()


def get_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine


def get_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_local()


def initialize_information(db: Session):
    import models.order as models
    count = db.query(models.Order).count()
    if count > 0:
        return

    order = models.Order(user_id=1,
                         item_description="Resma A4",
                         item_quantity=2,
                         item_price=9.99,
                         total_value=2 * 9.99)
    db.add(order)
    order = models.Order(user_id=1,
                         item_description="Caneta BIC",
                         item_quantity=5,
                         item_price=1,
                         total_value=5)
    db.add(order)
    order = models.Order(user_id=1,
                         item_description="Grampeador",
                         item_quantity=1,
                         item_price=15,
                         total_value=15)
    db.add(order)
    db.commit()
