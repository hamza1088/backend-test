from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Type, Callable, Union
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(debug=True)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbDependency: Type[Union[Session, Callable]] = Depends(get_db)

db_dependency: DbDependency = Depends(get_db)

@app.get("/")
def read_root():
    return {"message": "Success!"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)


@app.post("/seed-data")
async def seed_data_endpoint(db: Session = Depends(get_db)):
    import seed_data

    num_categories = 5
    num_products = 200
    num_sales = 1000
    num_inventory_entries = 400

    seed_data.seed_categories(db, num_categories)
    seed_data.seed_products(db, num_products)
    seed_data.seed_sales(db, num_sales)
    seed_data.seed_inventory(db, num_inventory_entries)

    return {"message": "Data seeding completed."}