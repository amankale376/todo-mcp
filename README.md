# Todo MCP Server

An MCP (Model Context Protocol) server that provides to-do list management functionality with MongoDB backend.

## Features

- **CRUD Operations**: Create, read, update, and delete to-do items
- **Status Management**: Mark items as completed or pending
- **MongoDB Integration**: Persistent storage using MongoDB
- **FastAPI Backend**: RESTful API endpoints for all operations

## Tools Available

- `add_todo`: Add a new to-do item
- `get_all_todos`: Retrieve all to-do items
- `update_todo`: Update an existing to-do item
- `delete_todo`: Delete a to-do item
- `toggle_todo_status`: Toggle completion status of a to-do item

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Set up MongoDB connection string in environment variables:
```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DATABASE="todo_db"
```

3. Run the server:
```bash
python -m todo_mcp_server.server
```

## Configuration

The server requires the following environment variables:
- `MONGODB_URI`: MongoDB connection string
- `MONGODB_DATABASE`: Database name (default: "todo_db")

## Usage

Once configured as an MCP server, you can use the tools to manage your to-do list:

- Add items with descriptions and optional due dates
- Mark items as completed or pending
- Update item details
- Delete items you no longer need
- View all items with their current status