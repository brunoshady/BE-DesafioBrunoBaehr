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
    import models.user as models
    count = db.query(models.User).count()
    if count > 0:
        return

    db_user = models.User(name='QnJ1bm8gQmFlaHI=',
                          cpf='MDU4LjUyMS43MjktNzk=',
                          email='shady.bnu@gmail.com',
                          phone_number='KDQ3KSA5OTYwNjA2MDc=')
    db.add(db_user)
    db_user = models.User(name='RnVsYW5vIGRhIFNpbHZh',
                          cpf='MTIzLjQ1Ni43ODktMTI=',
                          email='email@gmail.com',
                          phone_number='KDQ3KSA5OTkxMjM5NDM=')
    db.add(db_user)
    db_user = models.User(name='RGFsdmEgRWxpIFBhbmluaQ==',
                          cpf='Njc1LjQzNC43NzQtMTI=',
                          email='teste@gmail.com',
                          phone_number='KDQ3KSA5OTkyMzkxMTM=')
    db.add(db_user)

    db.commit()
