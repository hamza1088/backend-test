from fastapi import APIRouter, HTTPException
from database import SessionLocal
import seed_data

router = APIRouter()

@router.post("/data/seed")
async def seed_data_endpoint():
    num_categories = 5
    num_products = 200
    num_sales = 1000
    num_inventory_entries = 400
    db = SessionLocal()

    try:
        seed_data.seed_categories(db, num_categories)
        seed_data.seed_products(db, num_products)
        seed_data.seed_sales(db, num_sales)
        seed_data.seed_inventory(db, num_inventory_entries)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Data seeding failed")
    finally:
        db.close()

    return {"message": "Data seeding completed."}
