from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from shop_api.routers import item, cart

app = FastAPI(title="Shop API")

app.include_router(item.router)
app.include_router(cart.router)

Instrumentator().instrument(app).expose(app, include_in_schema=False)
