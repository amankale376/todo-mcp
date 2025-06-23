"""Database connection and operations for the Todo MCP Server."""

import os
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from .models import TodoItem, TodoCreate, TodoUpdate


class TodoDatabase:
    """Database handler for todo operations."""
    
    def __init__(self):
        """Initialize database connection."""
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGODB_DATABASE", "todo_db")
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        
    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.database = self.client[self.database_name]
            self.collection = self.database["todos"]
            # Test the connection
            self.client.admin.command('ping')
            print(f"Connected to MongoDB at {self.mongodb_uri}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoItem:
        """Create a new todo item."""
        if not self.collection:
            raise RuntimeError("Database not connected")
        
        todo_dict = todo_data.dict()
        todo_dict["created_at"] = datetime.utcnow()
        todo_dict["updated_at"] = datetime.utcnow()
        todo_dict["completed"] = False
        
        result = self.collection.insert_one(todo_dict)
        todo_dict["_id"] = result.inserted_id
        
        return TodoItem(**todo_dict)
    
    async def get_all_todos(self) -> List[TodoItem]:
        """Get all todo items."""
        if not self.collection:
            raise RuntimeError("Database not connected")
        
        todos = []
        for todo_doc in self.collection.find():
            todos.append(TodoItem(**todo_doc))
        
        return todos
    
    async def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Get a todo item by ID."""
        if not self.collection:
            raise RuntimeError("Database not connected")
        
        try:
            object_id = ObjectId(todo_id)
            todo_doc = self.collection.find_one({"_id": object_id})
            
            if todo_doc:
                return TodoItem(**todo_doc)
            return None
        except Exception:
            return None
    
    async def update_todo(self, todo_id: str, todo_update: TodoUpdate) -> Optional[TodoItem]:
        """Update a todo item."""
        if not self.collection:
            raise RuntimeError("Database not connected")
        
        try:
            object_id = ObjectId(todo_id)
            update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
            
            if update_data:
                update_data["updated_at"] = datetime.utcnow()
                
                result = self.collection.update_one(
                    {"_id": object_id},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    return await self.get_todo_by_id(todo_id)
            
            return None
        except Exception:
            return None
    
    async def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item."""
        if not self.collection:
            raise RuntimeError("Database not connected")
        
        try:
            object_id = ObjectId(todo_id)
            result = self.collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def toggle_todo_status(self, todo_id: str) -> Optional[TodoItem]:
        """Toggle the completion status of a todo item."""
        todo = await self.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        update_data = TodoUpdate(completed=not todo.completed)
        return await self.update_todo(todo_id, update_data)


# Global database instance
db = TodoDatabase()