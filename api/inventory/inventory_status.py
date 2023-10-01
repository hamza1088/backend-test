from fastapi import APIRouter, Query, HTTPException
from models import Inventory
from datetime import datetime
from pydantic import BaseModel
from database import SessionLocal
from api.jwt.jwt_authentication import verify_token

router = APIRouter()

@router.get("/")
async def view_inventory(low_stock_threshold: int,     token: str = Query(description="Token"),
):
    db = SessionLocal()
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Token invalid")
    try:
        inventory = db.query(Inventory).filter(Inventory.current_stock <= low_stock_threshold).all()

        inventory_status = [{"product_id": item.product_id, "current_stock": item.current_stock} for item in inventory]

        return inventory_status
    finally:
        db.close()

class InventoryUpdate(BaseModel):
    product_id: int
    new_stock_level: int


@router.put("/update")
def update_inventory(inventory_update: InventoryUpdate):
    db = SessionLocal()
    try:
        inventory_entry = db.query(Inventory).filter(Inventory.product_id == inventory_update.product_id).first()

        new_stock_level = inventory_update.new_stock_level
        inventory_entry.current_stock = new_stock_level

        inventory_entry.last_updated = datetime.utcnow()

        db.commit()

        return {"message": "Inventory updated successfully"}
    finally:
        db.close()