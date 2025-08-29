from fastapi import FastAPI
from app.api.v1 import users_route
from app.core.database import Base, engine

app = FastAPI(title="Growth Seeker Academy")

app.include_router(users_route.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "API is running!"}