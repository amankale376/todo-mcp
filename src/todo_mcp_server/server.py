#!/usr/bin/env python3
"""Todo MCP Server - Main server implementation."""

import asyncio
import json
import sys
from datetime import datetime
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)

from .database import db
from .models import TodoCreate, TodoUpdate


# Initialize the MCP server
server = Server("todo-mcp-server")


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="add_todo",
                description="Add a new todo item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the todo item"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the todo item"
                        },
                        "due_date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Due date for the todo item (ISO format)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Priority level",
                            "default": "medium"
                        }
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="get_all_todos",
                description="Get all todo items",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            ),
            Tool(
                name="update_todo",
                description="Update an existing todo item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of the todo item to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title of the todo item"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description of the todo item"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Whether the todo item is completed"
                        },
                        "due_date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "New due date for the todo item (ISO format)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "New priority level"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="delete_todo",
                description="Delete a todo item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of the todo item to delete"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="toggle_todo_status",
                description="Toggle the completion status of a todo item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of the todo item to toggle"
                        }
                    },
                    "required": ["todo_id"]
                }
            )
        ]
    )


@server.call_tool()
async def call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool calls."""
    try:
        if request.name == "add_todo":
            return await handle_add_todo(request.arguments)
        elif request.name == "get_all_todos":
            return await handle_get_all_todos()
        elif request.name == "update_todo":
            return await handle_update_todo(request.arguments)
        elif request.name == "delete_todo":
            return await handle_delete_todo(request.arguments)
        elif request.name == "toggle_todo_status":
            return await handle_toggle_todo_status(request.arguments)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {request.name}")],
                isError=True
            )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )


async def handle_add_todo(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle adding a new todo item."""
    title = arguments.get("title")
    description = arguments.get("description")
    due_date_str = arguments.get("due_date")
    priority = arguments.get("priority", "medium")
    
    if not title:
        return CallToolResult(
            content=[TextContent(type="text", text="Title is required")],
            isError=True
        )
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        except ValueError:
            return CallToolResult(
                content=[TextContent(type="text", text="Invalid due_date format. Use ISO format.")],
                isError=True
            )
    
    todo_data = TodoCreate(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority
    )
    
    todo = await db.create_todo(todo_data)
    
    return CallToolResult(
        content=[TextContent(
            type="text",
            text=f"Todo item created successfully:\n{format_todo(todo)}"
        )]
    )


async def handle_get_all_todos() -> CallToolResult:
    """Handle getting all todo items."""
    todos = await db.get_all_todos()
    
    if not todos:
        return CallToolResult(
            content=[TextContent(type="text", text="No todo items found.")]
        )
    
    todos_text = "All Todo Items:\n\n"
    for i, todo in enumerate(todos, 1):
        todos_text += f"{i}. {format_todo(todo)}\n\n"
    
    return CallToolResult(
        content=[TextContent(type="text", text=todos_text.strip())]
    )


async def handle_update_todo(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle updating a todo item."""
    todo_id = arguments.get("todo_id")
    
    if not todo_id:
        return CallToolResult(
            content=[TextContent(type="text", text="todo_id is required")],
            isError=True
        )
    
    # Parse due_date if provided
    due_date = None
    due_date_str = arguments.get("due_date")
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        except ValueError:
            return CallToolResult(
                content=[TextContent(type="text", text="Invalid due_date format. Use ISO format.")],
                isError=True
            )
    
    update_data = TodoUpdate(
        title=arguments.get("title"),
        description=arguments.get("description"),
        completed=arguments.get("completed"),
        due_date=due_date,
        priority=arguments.get("priority")
    )
    
    updated_todo = await db.update_todo(todo_id, update_data)
    
    if not updated_todo:
        return CallToolResult(
            content=[TextContent(type="text", text="Todo item not found or no changes made")],
            isError=True
        )
    
    return CallToolResult(
        content=[TextContent(
            type="text",
            text=f"Todo item updated successfully:\n{format_todo(updated_todo)}"
        )]
    )


async def handle_delete_todo(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle deleting a todo item."""
    todo_id = arguments.get("todo_id")
    
    if not todo_id:
        return CallToolResult(
            content=[TextContent(type="text", text="todo_id is required")],
            isError=True
        )
    
    success = await db.delete_todo(todo_id)
    
    if not success:
        return CallToolResult(
            content=[TextContent(type="text", text="Todo item not found")],
            isError=True
        )
    
    return CallToolResult(
        content=[TextContent(type="text", text="Todo item deleted successfully")]
    )


async def handle_toggle_todo_status(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle toggling todo completion status."""
    todo_id = arguments.get("todo_id")
    
    if not todo_id:
        return CallToolResult(
            content=[TextContent(type="text", text="todo_id is required")],
            isError=True
        )
    
    updated_todo = await db.toggle_todo_status(todo_id)
    
    if not updated_todo:
        return CallToolResult(
            content=[TextContent(type="text", text="Todo item not found")],
            isError=True
        )
    
    status = "completed" if updated_todo.completed else "pending"
    return CallToolResult(
        content=[TextContent(
            type="text",
            text=f"Todo item status toggled to {status}:\n{format_todo(updated_todo)}"
        )]
    )


def format_todo(todo) -> str:
    """Format a todo item for display."""
    status = "✅ Completed" if todo.completed else "⏳ Pending"
    due_date_str = f" (Due: {todo.due_date.strftime('%Y-%m-%d %H:%M')})" if todo.due_date else ""
    priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(todo.priority, "🟡")
    
    result = f"ID: {str(todo.id)}\n"
    result += f"Title: {todo.title}\n"
    result += f"Status: {status}\n"
    result += f"Priority: {priority_emoji} {todo.priority.title()}\n"
    
    if todo.description:
        result += f"Description: {todo.description}\n"
    
    result += f"Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    result += f"Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M')}{due_date_str}"
    
    return result


async def main():
    """Main entry point for the server."""
    # Connect to database
    try:
        db.connect()
    except Exception as e:
        print(f"Failed to connect to database: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    finally:
        # Disconnect from database
        db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())