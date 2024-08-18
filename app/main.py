from fastapi import FastAPI
from app.api.v1 import routes
from app.api.v1.database import engine, Base

app = FastAPI()

# Automatically create the SQLite database and tables
Base.metadata.create_all(bind=engine)

# Include the v1 API routes
app.include_router(routes.router, prefix="/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Management API"}
