from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware  

from .database.database import create_db
from .routers import sensors, blocks, measurements


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield
   


app = FastAPI(
    title="Johannan AnturiAPI",
    description="REST-rajapinta tehdashallin lämpötila-antureiden datan keräämiseen ja hallintaan.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #toimii kaikki
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(blocks.router)
app.include_router(measurements.router)


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Tervetuloa Johannan AnturiAPI:iin",
        "documentation": "/docs",
        "version": "1.0.0"
    }
