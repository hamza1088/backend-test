from fastapi import APIRouter, Query
from sqlalchemy.orm import joinedload
from models import Product, Sale
from datetime import date
from database import SessionLocal
from api.sales.responses.sales_response import SaleResponse


router = APIRouter()

@router.get("/sales/")
async def get_sales(
    start_date: date = Query(..., description="Start date of the date range"),
    end_date: date = Query(..., description="End date of the date range"),
    product_id: int = Query(None, description="Product ID"),
    category_id: int = Query(None, description="Category ID"),
):
    db = SessionLocal()
    try:
        query = db.query(Sale)

        if start_date and end_date:
            query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
        if product_id:
            query = query.filter(Sale.product_id == product_id)
        if category_id:
            query = query.filter(Sale.product.has(Product.category_id == category_id))

        query = query.options(joinedload(Sale.product).joinedload(Product.category))

        sales = []
        for sale in query.all():
            sale_response = SaleResponse(
                product_id=sale.product.product_id,
                quantity_sold=sale.quantity_sold,
                created_at=sale.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                sale_date=sale.sale_date,
                sale_id=sale.sale_id,
                product_name=sale.product.product_name,
                category_name=sale.product.category.category_name,
            )
            sales.append(sale_response)

        return sales
    finally:
        db.close()




