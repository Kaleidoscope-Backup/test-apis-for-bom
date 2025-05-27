from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(title="Inventory Management API", version="1.0.0")

# Data Models
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

# Example data
inventory = {
    1: {"name": "Laptop", "description": "A gaming laptop", "price": 1500.00, "quantity": 10},
    2: {"name": "Mouse", "description": "Wireless mouse", "price": 25.50, "quantity": 100},
}

# Endpoints

@app.get("/items", tags=["Inventory"])
def get_all_items():
    """
    Get a list of all items in the inventory.
    """
    return inventory

@app.get("/items/{item_id}", tags=["Inventory"])
def get_item(item_id: int):
    """
    Get details of a single item by its ID.
    """
    item = inventory.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", tags=["Inventory"])
def create_item(item: Item):
    """
    Add a new item to the inventory.
    """
    inventory[item.id] = item.dict()
    return {"message": "Item created successfully", "item": item}

@app.put("/items/{item_id}", tags=["Inventory"])
def update_item(item_id: int, updated_item: Item):
    """
    Update an existing item by its ID.
    """
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = updated_item.dict()
    return {"message": "Item updated successfully", "item": updated_item}

@app.delete("/items/{item_id}", tags=["Inventory"])
def delete_item(item_id: int):
    """
    Delete an item from the inventory by its ID.
    """
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory[item_id]
    return {"message": "Item deleted successfully"}

@app.get("/search", tags=["Inventory"])
def search_items(query: str = Query(..., description="Search query")):
    """
    Search for items by name (vulnerable to SQL injection for SAST detection)
    """
    # This is intentionally vulnerable code for SAST tool detection
    # DO NOT USE IN PRODUCTION - FOR TESTING PURPOSES ONLY
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    # VULNERABILITY: Unsanitized input used in SQL query
    sql = f"SELECT * FROM items WHERE name LIKE '%{query}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return {"results": results}

@app.get("/system-check", tags=["System"])
def system_check(command: str = Query("echo 'system check'", description="System command to run")):
    """
    Execute a system command and return the result (CRITICAL VULNERABILITY - DO NOT USE IN PRODUCTION)
    """
    # This is intentionally vulnerable code for SAST tool detection
    # DO NOT USE IN PRODUCTION - FOR TESTING PURPOSES ONLY
    
    # VULNERABILITY: Unsanitized input directly passed to os.system
    result = os.popen(command).read()
    return {"output": result}
