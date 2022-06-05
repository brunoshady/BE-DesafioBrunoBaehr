import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models.user as models
import repositories.user as user_repository
import repositories.order as order_repository
import schemas.user as schemas
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


@app.get("/")
async def root():
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/users/", response_model=list[schemas.User], response_class=PrettyJSONResponse)
async def get_users(db: Session = Depends(get_db)):
    try:
        users = user_repository.get_users(db)
        if not len(users):
            return JSONResponse(content={'detail': 'No users found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return users


@app.get("/users/{user_id}", response_model=schemas.User, response_class=PrettyJSONResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = user_repository.get_user_by_id(db, user_id)
        if user is None:
            return JSONResponse(content={'detail': 'User not found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user


@app.get("/users/{user_id}/orders/", response_class=PrettyJSONResponse)
async def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    try:
        user = user_repository.get_user_by_id(db, user_id)
        if user is None:
            return JSONResponse(content={'detail': 'User not found!'}, status_code=404)

        orders = order_repository.get_orders_by_user(user_id)
        if orders is None:
            return JSONResponse(content={'detail': 'Orders not found!'}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return orders


@app.post("/users/", status_code=201, response_model=schemas.User, response_class=PrettyJSONResponse)
async def create_user(schema_user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_repository.create(db, schema_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user


@app.patch("/users/{user_id}", response_class=PrettyJSONResponse)
async def update_user(user_id: int, schema_user: schemas.UserPatch, db: Session = Depends(get_db)):
    try:
        user = user_repository.update(db, user_id, schema_user)
        if not user:
            return JSONResponse(content='User not found!', status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user


@app.delete("/users/{user_id}", response_class=PrettyJSONResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_repository.delete(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'detail': 'User deleted!'}


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=get_engine())
    initialize_information(next(get_db()))
    uvicorn.run("__main__:app", host="0.0.0.0", port=8080, reload=True, workers=2)
