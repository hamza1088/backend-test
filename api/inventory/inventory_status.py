from fastapi import APIRouter
from models import Inventory
from datetime import datetime
from pydantic import BaseModel
from database import SessionLocal

router = APIRouter()

@router.get("/inventory")
async def view_inventory(low_stock_threshold: int = 10):
    db = SessionLocal()
    try:
        inventory = db.query(Inventory).filter(Inventory.current_stock <= low_stock_threshold).all()

        inventory_status = [{"product_id": item.product_id, "current_stock": item.current_stock} for item in inventory]

        return inventory_status
    finally:
        db.close()

class InventoryUpdate(BaseModel):
    product_id: int
    new_stock_level: int


@router.put("/inventory/update")
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