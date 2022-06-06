import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models.order as models
import repositories.user as user_repository
import repositories.order as order_repository
import schemas.order as schemas
from database import initialize_information, get_session, get_engine
from utils.json_response import PrettyJSONResponse

app = FastAPI()


# Dependency
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_user():
    return None


@app.get("/")
async def root():
    return RedirectResponse(url="/orders/", status_code=303)


@app.get("/orders/", response_model=list[schemas.Order], response_class=PrettyJSONResponse)
async def get_orders(db: Session = Depends(get_db)):
    try:
        orders = order_repository.get_orders(db)
        if not len(orders):
            return JSONResponse(content={'detail': 'No orders found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order, response_class=PrettyJSONResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = order_repository.get_by_id(db, order_id)
        if order is None:
            return JSONResponse(content={'detail': 'Order not found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return order


@app.get("/orders/user/{user_id}/", response_model=list[schemas.Order], response_class=PrettyJSONResponse)
async def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        order_list = order_repository.get_by_user_id(db, user_id)
        if not len(order_list):
            return JSONResponse(content={'detail': 'No orders found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return order_list


@app.post("/orders/", status_code=201, response_model=schemas.Order, response_class=PrettyJSONResponse)
async def create_order(schema_order: schemas.OrderCreate, db: Session = Depends(get_db), mock_user=Depends(get_user)):
    try:
        user = user_repository.get_user_by_id(schema_order.user_id, mock_user)
        if not user:
            return JSONResponse(content={'detail': 'User not found!'}, status_code=404)

        order = order_repository.create(db, schema_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return order


@app.patch("/orders/{order_id}", response_class=PrettyJSONResponse)
async def update_order(order_id: int, schema_order: schemas.OrderPatch, db: Session = Depends(get_db), mock_user=Depends(get_user)):
    try:
        if schema_order.user_id is not None:
            user = user_repository.get_user_by_id(schema_order.user_id, mock_user)
            if not user:
                return JSONResponse(content={'detail': 'User not found!'}, status_code=404)

        order = order_repository.update(db, order_id, schema_order)
        if not order:
            return JSONResponse(content={'detail': 'Order not found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return order


@app.delete("/orders/{order_id}", response_class=PrettyJSONResponse)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        result = order_repository.delete(db, order_id)
        if not result:
            return JSONResponse(content={'detail': 'Order not found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'detail': 'Order deleted!'}


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=get_engine())
    initialize_information(next(get_db()))
    uvicorn.run("__main__:app", host="0.0.0.0", port=8090, reload=True, workers=2)
