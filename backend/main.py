from datetime import date
from itertools import count
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Window Garden API")

# Allow the React dev server to call the API directly if the proxy isn't used.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlantIn(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    water_every_days: int = Field(ge=1, le=60)


class Plant(PlantIn):
    id: int
    last_watered: Optional[str] = None  # ISO date


# Simple in-memory storage (resets when the server restarts).
_ids = count(4)
plants: dict[int, Plant] = {
    1: Plant(id=1, name="Monstera", water_every_days=7),
    2: Plant(id=2, name="Snake plant", water_every_days=14),
    3: Plant(id=3, name="Basil", water_every_days=2),
}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/plants", response_model=list[Plant])
def list_plants():
    return list(plants.values())


@app.post("/api/plants", response_model=Plant, status_code=201)
def add_plant(body: PlantIn):
    plant = Plant(id=next(_ids), **body.model_dump())
    plants[plant.id] = plant
    return plant


@app.post("/api/plants/{plant_id}/water", response_model=Plant)
def water_plant(plant_id: int):
    plant = plants.get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.last_watered = date.today().isoformat()
    return plant


@app.delete("/api/plants/{plant_id}", status_code=204)
def delete_plant(plant_id: int):
    if plant_id not in plants:
        raise HTTPException(status_code=404, detail="Plant not found")
    del plants[plant_id]
