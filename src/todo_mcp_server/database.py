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
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.database_name = os.getenv("MONGODB_DATABASE", "todo_db")
        self.use_memory = os.getenv("USE_MEMORY_DB", "false").lower() == "true"
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self.connected = False
        self.memory_store = []  # In-memory fallback
        
    def _ensure_connection(self):
        """Ensure database connection is established (lazy connection)."""
        if self.connected:
            return
            
        if self.use_memory or not self.mongodb_uri:
            print("🔄 Using in-memory storage (no MongoDB connection)")
            self.connected = True
            return
            
        self.connect()
        
    def connect(self):
        """Connect to MongoDB."""
        if not self.mongodb_uri:
            print("⚠️  No MONGODB_URI provided, falling back to in-memory storage")
            self.use_memory = True
            self.connected = True
            return
            
        try:
            print(f"Attempting to connect to MongoDB...")
            print(f"URI: {self.mongodb_uri[:20]}...")  # Only show first 20 chars for security
            print(f"Database: {self.database_name}")
            
            self.client = MongoClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            self.database = self.client[self.database_name]
            self.collection = self.database["todos"]
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"✅ Successfully connected to MongoDB!")
            print(f"Database: {self.database_name}")
            print(f"Collection: todos")
            self.connected = True
            
        except Exception as e:
            print(f"⚠️  Failed to connect to MongoDB: {str(e)}")
            print("🔄 Falling back to in-memory storage")
            self.use_memory = True
            self.connected = True
            self.client = None
            self.database = None
            self.collection = None
    
    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoItem:
        """Create a new todo item."""
        self._ensure_connection()
        
        todo_dict = todo_data.dict()
        todo_dict["created_at"] = datetime.utcnow()
        todo_dict["updated_at"] = datetime.utcnow()
        todo_dict["completed"] = False
        
        if self.use_memory:
            # In-memory storage
            from bson import ObjectId
            todo_dict["_id"] = ObjectId()
            self.memory_store.append(todo_dict.copy())
        else:
            # MongoDB storage
            if not self.collection:
                raise RuntimeError("Database not connected")
            result = self.collection.insert_one(todo_dict)
            todo_dict["_id"] = result.inserted_id
        
        return TodoItem(**todo_dict)
    
    async def get_all_todos(self) -> List[TodoItem]:
        """Get all todo items."""
        self._ensure_connection()
        
        todos = []
        if self.use_memory:
            # In-memory storage
            for todo_doc in self.memory_store:
                todos.append(TodoItem(**todo_doc))
        else:
            # MongoDB storage
            if not self.collection:
                raise RuntimeError("Database not connected")
            for todo_doc in self.collection.find():
                todos.append(TodoItem(**todo_doc))
        
        return todos
    
    async def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Get a todo item by ID."""
        self._ensure_connection()
        
        try:
            object_id = ObjectId(todo_id)
            
            if self.use_memory:
                # In-memory storage
                for todo_doc in self.memory_store:
                    if todo_doc["_id"] == object_id:
                        return TodoItem(**todo_doc)
                return None
            else:
                # MongoDB storage
                if not self.collection:
                    raise RuntimeError("Database not connected")
                todo_doc = self.collection.find_one({"_id": object_id})
                if todo_doc:
                    return TodoItem(**todo_doc)
                return None
        except Exception:
            return None
    
    async def update_todo(self, todo_id: str, todo_update: TodoUpdate) -> Optional[TodoItem]:
        """Update a todo item."""
        self._ensure_connection()
        
        try:
            object_id = ObjectId(todo_id)
            update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
            
            if not update_data:
                return None
                
            update_data["updated_at"] = datetime.utcnow()
            
            if self.use_memory:
                # In-memory storage
                for i, todo_doc in enumerate(self.memory_store):
                    if todo_doc["_id"] == object_id:
                        self.memory_store[i].update(update_data)
                        return TodoItem(**self.memory_store[i])
                return None
            else:
                # MongoDB storage
                if not self.collection:
                    raise RuntimeError("Database not connected")
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
        self._ensure_connection()
        
        try:
            object_id = ObjectId(todo_id)
            
            if self.use_memory:
                # In-memory storage
                for i, todo_doc in enumerate(self.memory_store):
                    if todo_doc["_id"] == object_id:
                        del self.memory_store[i]
                        return True
                return False
            else:
                # MongoDB storage
                if not self.collection:
                    raise RuntimeError("Database not connected")
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