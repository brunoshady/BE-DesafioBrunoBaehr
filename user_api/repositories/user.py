from sqlalchemy.orm import Session

import models.user as models
import schemas.user as schemas

from utils.security import Security
from cache.cache import Cache


def get_users(db: Session):
    try:
        user_list = db.query(models.User).order_by(models.User.id.desc()).all()
        for user in user_list:
            user = Security().decrypt_user(user)
            Cache().save_cache(user.id, user)
    except Exception as e:
        raise e

    return user_list


def get_user_by_id(db: Session, user_id: int):
    try:
        cached_user = Cache().get_cache(user_id)
        if cached_user:
            return cached_user

        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            return None

        decrypted_user = Security().decrypt_user(user)
        Cache().save_cache(user_id, decrypted_user)
    except Exception as e:
        raise e

    return decrypted_user


def create(db: Session, schema_user: schemas.UserCreate):
    try:
        user = models.User()
        for key, value in schema_user.dict(exclude_unset=True).items():
            setattr(user, key, value)

        if user.name == '' or not user.name:
            raise Exception('Name could not be empty!')
        if user.cpf == '' or not user.cpf:
            raise Exception('CPF could not be empty!')

        encrypted_user = Security().encrypt_user(user)
        db.add(encrypted_user)
        db.commit()
        db.refresh(encrypted_user)
        user = Security().decrypt_user(encrypted_user)
        Cache().save_cache(user.id, user)
    except Exception as e:
        raise e

    return user


def update(db: Session, user_id: int, schema_user: schemas.UserPatch):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return None

        decrypted_user = Security().decrypt_user(user)
        for key, value in schema_user.dict(exclude_unset=True).items():
            setattr(decrypted_user, key, value)

        if user.name == '' or not user.name:
            raise Exception('Name could not be empty!')
        if user.cpf == '' or not user.cpf:
            raise Exception('CPF could not be empty!')

        encrypted_user = Security().encrypt_user(decrypted_user)
        db.add(encrypted_user)
        db.commit()
        db.refresh(encrypted_user)
        user = Security().decrypt_user(user)
        Cache().save_cache(user.id, user)
    except Exception as e:
        raise e

    return user


def delete(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise Exception("User not found!")

        db.delete(user)
        db.commit()
        Cache().delete_cache(user_id)
    except Exception as e:
        raise e
