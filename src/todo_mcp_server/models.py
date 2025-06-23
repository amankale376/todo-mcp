"""Data models for the Todo MCP Server."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TodoItem(BaseModel):
    """Todo item model."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., description="Title of the todo item")
    description: Optional[str] = Field(None, description="Detailed description of the todo item")
    completed: bool = Field(default=False, description="Whether the todo item is completed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo item")
    priority: str = Field(default="medium", description="Priority level: low, medium, high")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TodoCreate(BaseModel):
    """Model for creating a new todo item."""
    
    title: str = Field(..., description="Title of the todo item")
    description: Optional[str] = Field(None, description="Detailed description of the todo item")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo item")
    priority: str = Field(default="medium", description="Priority level: low, medium, high")


class TodoUpdate(BaseModel):
    """Model for updating an existing todo item."""
    
    title: Optional[str] = Field(None, description="Title of the todo item")
    description: Optional[str] = Field(None, description="Detailed description of the todo item")
    completed: Optional[bool] = Field(None, description="Whether the todo item is completed")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo item")
    priority: Optional[str] = Field(None, description="Priority level: low, medium, high")