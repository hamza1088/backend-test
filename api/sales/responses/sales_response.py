from pydantic import BaseModel

class SaleResponse(BaseModel):
    product_id: int
    quantity_sold: int
    created_at: str
    sale_date: str
    sale_id: int
    product_name: str
    category_name: str