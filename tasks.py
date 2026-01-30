from bson import ObjectId
from celery_worker import celery_app
import pymongo  # For your DB tasks
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

@celery_app.task
def reset_inventory_data(inventory_id: str, new_quantity: int):
    client = pymongo.MongoClient(MONGODB_URL)
    db = client['fruit_supply_db']
    inventory_collection = db['inventory']
    inventory_collection.update_one(
            {"_id": ObjectId(inventory_id)},
            {"$set": {"quantity": new_quantity}}
        )
    return "Reset inventory data"
# Schedule in celery_app.conf.beat_schedule below




