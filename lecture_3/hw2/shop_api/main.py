from fastapi import FastAPI
from ..shop_api.api.cart.routes import router as cart_router
from ..shop_api.api.item.routes import router as item_router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Shop API")
Instrumentator().instrument(app).expose(app)


app.include_router(cart_router)
app.include_router(item_router)
