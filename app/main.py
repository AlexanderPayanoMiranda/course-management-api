from fastapi import FastAPI
from app.api.v1 import routes as routes_v1
from app.api.v2 import routes as routes_v2
from app.api.v1.database import engine, Base

app = FastAPI()

# Automatically create the SQLite database and tables
Base.metadata.create_all(bind=engine)

app.include_router(routes_v1.router, prefix="/v1")
app.include_router(routes_v2.router, prefix="/v2")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Management API"}
