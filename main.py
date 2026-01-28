from typing import Optional
from bson import ObjectId
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from pymongo import MongoClient


# Configuring FastAPI application
proj = FastAPI(title='Fruit Supply Project')

# Defining pydantic models for fruit data
class Fruit(BaseModel):
    fruit_id: ObjectId = None  # Unique identifier for the fruit
    name: str
    region: str
    season: str
    shelf_life_days: int
    price: float
    ripe: bool

class OrderRequest(BaseModel):
    order_id: ObjectId # Unique identifier for the order
    fruit_name: str
    quantity: int
    delivery_address: str
    total_price: float
    delivery_type: str  # e.g., "standard", "express"
    comments: Optional[str] = None

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["fruit_supply_db"]
fruits_collection = db["fruits"]
orders_collection = db["orders"]


# Writing API endpoints
@proj.get("/", response_class=HTMLResponse)
def homepage():
    return """
            <h1>Welcome to the Fruit Supply Project!</h1>
            <p>Your go-to solution for managing and enhancing fruit supply chain operations.</p>
    """

@proj.post("/add_fruit")
def add_fruit(fruit: Fruit):
    fruit_dict = json.loads(fruit.json())

    result = fruits_collection.insert_one(fruit_dict)
    return {"message": "Fruit added successfully", "fruit_id": str(result.inserted_id)}


if __name__ == "__main__":
    uvicorn.run(proj, host="localhost", port=8000)