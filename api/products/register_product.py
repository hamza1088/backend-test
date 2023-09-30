from fastapi import HTTPException, APIRouter
from models import Product
from database import SessionLocal
from pydantic import BaseModel


router = APIRouter()
class ProductCreate(BaseModel):
    product_name: str
    category_id: int
    unit_price: float
    description: str

@router.post("/products/register")
async def create_product(product: ProductCreate):
    db = SessionLocal()

    try:
        new_product = Product(**product.dict())

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")