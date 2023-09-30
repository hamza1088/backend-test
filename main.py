from fastapi import FastAPI
import models
from database import engine
from api.sales.sales_status import router as sales_status_router
from api.revenue.analyze_revenue import router as analyze_revenue_router
from api.products.register_product import router as register_product_router
from api.inventory.inventory_status import router as analyze_inventory_router
from api.jwt.jwt_authentication import router as jwt_router
from seeder import router as seeder_router

app = FastAPI(debug=True)
models.Base.metadata.create_all(bind=engine)

#Routes
app.include_router(seeder_router, prefix="/seeder", tags=["seeder"])
app.include_router(jwt_router, prefix="/auth", tags=["authetication"])
app.include_router(sales_status_router, prefix="/sales", tags=["sales"])
app.include_router(analyze_revenue_router, prefix="/revenue", tags=["revenue"])
app.include_router(register_product_router, prefix="/products", tags=["products"])
app.include_router(analyze_inventory_router, prefix="/inventory", tags=["inventory"])

