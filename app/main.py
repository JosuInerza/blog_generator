from fastapi import FastAPI
from app.api.v1.routes import router as items_router
from app.api.v1.validate_routes import router as validate_router

app = FastAPI(title="Blog Generator - API Skeleton")

app.include_router(items_router, prefix="/api/v1/items", tags=["items"])
app.include_router(validate_router, tags=["validate"])


@app.get("/")
def read_root():
    return {"message": "Blog Generator API. See /docs"}
