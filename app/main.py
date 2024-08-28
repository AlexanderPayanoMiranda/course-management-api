from fastapi import FastAPI
from app.api.v1 import routes as routes_v1
from app.api.v2 import routes as routes_v2
from app.api.v3 import routes as routes_v3
from app.api.v3.database import engine as engine_v3, Base as Base_v3

app = FastAPI()

# Automatically create the SQLite database and tables for v3
Base_v3.metadata.create_all(bind=engine_v3)

app.include_router(routes_v1.router, prefix="/v1")
app.include_router(routes_v2.router, prefix="/v2")
app.include_router(routes_v3.router, prefix="/v3")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Management API"}
