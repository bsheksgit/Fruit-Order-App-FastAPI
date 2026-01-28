from typing import Optional
import json

from bson.objectid import ObjectId
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from pymongo import MongoClient


# Configuring FastAPI application
proj = FastAPI(title='Fruit Supply Project')

# Defining pydantic models for fruit data
class Fruit(BaseModel):
    name: str
    region: str
    season: str
    shelf_life_days: int
    price: float
    ripe: bool

class OrderRequest(BaseModel):
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

#Defining DB constraints
fruits_collection.create_index("name", unique=True)

# Writing API endpoints
@proj.get("/", response_class=HTMLResponse)
def homepage():
    return """
            <h1>Welcome to the Fruit Supply Project!</h1>
            <p>Your go-to solution for managing and enhancing fruit supply chain operations.</p>
    """

@proj.post("/add_fruit")
def add_fruit(fruit: Fruit):
    """
    A POST endpoint to add a new fruit to the database.
    
    :param fruit: Description
    :type fruit: Fruit
    """

    fruit_dict = json.loads(fruit.json())

    try:
        result = fruits_collection.insert_one(fruit_dict)
        return {"message": "Fruit added successfully", "fruit_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": f"Error occurred while adding fruit to database: {str(e)}"}

@proj.get("/get_fruit/{fruit_name}")
def get_fruit(fruit_name: str):
    """
    A GET endpoint to retrieve a specific fruit by name.
    
    :param fruit_name: Name of the fruit to retrieve
    :type fruit_name: str
    """
    fruit = fruits_collection.find_one({"name": fruit_name})
    if not fruit:
        return {"error": "Fruit not found"}
    fruit["_id"] = str(fruit["_id"]) 
    return {"fruit": fruit}

@proj.patch("/update_fruit_price/{fruit_name}")
def update_fruit_price(fruit_name: str, new_price: float):
    """
    A PATCH endpoint to update the price of a specific fruit by name.
    
    :param fruit_name: Name of the fruit to update
    :type fruit_name: str
    :param new_price: New price for the fruit
    :type new_price: float
    """
    result = fruits_collection.update_one(
        {"name": fruit_name},
        {"$set": {"price": new_price}}
    )
    if result.matched_count == 0:
        return {"error": "Fruit not found"}
    
    return {"message": "Fruit price updated successfully"}

@proj.delete("/delete_fruit/{fruit_name}")
def delete_fruit(fruit_name: str):
    """
    A DELETE endpoint to delete a specific fruit by name.
    
    :param fruit_name: Name of the fruit to delete
    :type fruit_name: str
    """
    result = fruits_collection.delete_one({"name": fruit_name})
    if result.deleted_count == 0:
        return {"error": "Fruit not found"}
    
    return {"message": "Fruit deleted successfully"}

@proj.post("/place_order")
def place_order(order: OrderRequest):
    """
    A POST endpoint to place a new order for fruits.
    
    :param order: Order details
    :type order: OrderRequest
    """
    order_dict = json.loads(order.json())

    try:
        result = orders_collection.insert_one(order_dict)
        return {"message": "Order placed successfully", "order_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": f"Error occurred while placing order: {str(e)}"}

@proj.get("/get_order/{order_id}")
def get_order(order_id: str):
    """
    A GET endpoint to retrieve a specific order by ID.
    
    :param order_id: ID of the order to retrieve
    :type order_id: str
    """

    try:
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            return {"error": "Order not found"}
        order["_id"] = str(order["_id"]) 
        return {"order": order}
    except Exception as e:
        return {"error": f"Error occurred while retrieving order: {str(e)}"}

@proj.put("/update_order/{order_id}")
def update_order(order_id: str, order: OrderRequest):
    """
    A PUT endpoint to update an existing order by ID.
    
    :param order_id: ID of the order to update
    :type order_id: str
    :param order: Updated order details
    :type order: OrderRequest
    """
    order_dict = json.loads(order.json())

    try:
        result = orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": order_dict}
        )
        if result.matched_count == 0:
            return {"error": "Order not found"}
        return {"message": "Order updated successfully"}
    except Exception as e:
        return {"error": f"Error occurred while updating order: {str(e)}"}

@proj.delete("/delete_order/{order_id}")
def delete_order(order_id: str):
    """
    A DELETE endpoint to delete a specific order by ID.
    
    :param order_id: ID of the order to delete
    :type order_id: str
    """
    try:
        result = orders_collection.delete_one({"_id": ObjectId(order_id)})
        if result.deleted_count == 0:
            return {"error": "Order not found"}
        return {"message": "Order deleted successfully"}
    except Exception as e:
        return {"error": f"Error occurred while deleting order: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(proj, host="localhost", port=8000)