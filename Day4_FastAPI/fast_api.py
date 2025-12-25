"""A simple FastAPI application with multiple endpoints demonstrating CRUD operations."""
import fastapi

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    """Read the root endpoint and return a greeting message. Additional docstring for clarity."""
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Retrieve an item by its ID with optional query parameter."""
    return {"item_id": item_id, "q": q}
@app.post("/items/")
def create_item(item: dict):
    """Create a new item with the provided item data."""
    return item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    """Update an existing item by its ID."""
    return {"item_id": item_id, **item}
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by its ID."""
    return {"item_id": item_id, "status": "deleted"}
@app.get("/users/{user_id}")
def read_user(user_id: int):
    """Retrieve a user by their ID."""
    return {"user_id": user_id}
@app.post("/users/")
def create_user(user: dict):
    """Create a new user with the provided user data."""
    return user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: dict):
    """Update an existing user by their ID."""
    return {"user_id": user_id, **user}
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user by their ID."""
    return {"user_id": user_id, "status": "deleted"}
