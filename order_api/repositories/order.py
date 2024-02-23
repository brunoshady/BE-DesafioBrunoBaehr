from sqlalchemy.orm import Session

import models.order as models
import schemas.order as schemas

from cache.cache import Cache


def _validate_properties(order: models.Order):
    if order.item_description == '' or order.item_description is None:
        raise Exception('Item description could not be empty!')
    if order.item_quantity == 0 or order.item_quantity is None:
        raise Exception('Quantity could not be empty!')
    if order.item_price == 0 or order.item_price is None:
        raise Exception('Item price could not be empty!')


def get_orders(db: Session):
    try:
        order_list = db.query(models.Order).order_by(models.Order.id.desc()).all()
        for order in order_list:
            if isinstance(order, models.Order):
                Cache().save_order_cache(order.id, order.dict())
    except Exception as e:
        raise e

    return order_list


def get_by_id(db: Session, order_id: int):
    try:
        cached_order = Cache().get_order_cache(order_id)
        if cached_order:
            return cached_order

        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if order is None:
            return None

        Cache().save_order_cache(order.id, order.dict())
    except Exception as e:
        raise e

    return order


def get_by_user_id(db: Session, user_id: int):
    try:
        order_list = db.query(models.Order).filter(models.Order.user_id == user_id).order_by(
            models.Order.id.desc()).all()
        for order in order_list:
            if isinstance(order, models.Order):
                Cache().save_order_cache(order.id, order.dict())
    except Exception as e:
        raise e

    return order_list


def create(db: Session, schema_user: schemas.OrderCreate):
    try:
        order = models.Order()
        for key, value in schema_user.dict(exclude_unset=True).items():
            setattr(order, key, value)

        _validate_properties(order)
        # TODO - isso aqui deveria ser automatico no model
        order.total_value = order.item_price * order.item_quantity
        db.add(order)
        db.commit()
        db.refresh(order)
        Cache().save_order_cache(order.id, order.dict())
    except Exception as e:
        raise e

    return order


def update(db: Session, order_id: int, schema_user: schemas.OrderPatch):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            return None

        for key, value in schema_user.dict(exclude_unset=True).items():
            setattr(order, key, value)

        _validate_properties(order)
        # TODO - isso aqui deveria ser automatico no model
        order.total_value = order.item_price * order.item_quantity
        db.add(order)
        db.commit()
        db.refresh(order)
        Cache().save_order_cache(order.id, order.dict())
    except Exception as e:
        raise e

    return order


def delete(db: Session, order_id: int):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if order is None:
            return False

        db.delete(order)
        db.commit()
        Cache().delete_order_cache(order.id)
    except Exception as e:
        raise e

    return True
