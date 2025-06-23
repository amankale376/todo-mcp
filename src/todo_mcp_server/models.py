"""Data models for the Todo MCP Server."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2."""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, handler):
        field_schema.update(type="string", format="objectid")
        return field_schema


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
        populate_by_name = True
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