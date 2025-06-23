# Todo MCP Server

A Model Context Protocol (MCP) server that provides todo management functionality with support for both in-memory storage and MongoDB persistence.

## Features

- ✅ **Add Todo Items** - Create new todo items with title, description, due date, and priority
- 📋 **List All Todos** - Retrieve all todo items with formatted display
- ✏️ **Update Todos** - Modify existing todo items (title, description, completion status, etc.)
- 🗑️ **Delete Todos** - Remove todo items by ID
- 🔄 **Toggle Status** - Quick toggle between completed/pending status
- 💾 **Dual Storage** - Support for both in-memory storage and MongoDB persistence
- 🚀 **Lazy Loading** - Database connections established only when needed

## Storage Options

### 1. In-Memory Storage (Default)
Perfect for testing and development. No external dependencies required.

```bash
# Set environment variable
export USE_MEMORY_DB=true
```

### 2. MongoDB Storage
For persistent storage across server restarts.

```bash
# Set your MongoDB connection string
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
export MONGODB_DATABASE="todo_db"  # Optional, defaults to "todo_db"
```

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd todo-mcp-server
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### MCP Settings
The server is configured in your MCP settings file. Here's the recommended configuration:

```json
{
  "mcpServers": {
    "todo": {
      "command": "/path/to/todo-mcp-server/venv/bin/python",
      "args": ["-m", "todo_mcp_server.server"],
      "cwd": "/path/to/todo-mcp-server",
      "env": {
        "USE_MEMORY_DB": "true",
        "MONGODB_DATABASE": "todo_db",
        "PYTHONPATH": "/path/to/todo-mcp-server/src"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### MongoDB Configuration
To use MongoDB instead of in-memory storage:

1. **Remove or set `USE_MEMORY_DB` to `false`**
2. **Add your MongoDB URI:**
   ```json
   "env": {
     "MONGODB_URI": "your-mongodb-connection-string",
     "MONGODB_DATABASE": "todo_db",
     "PYTHONPATH": "/path/to/todo-mcp-server/src"
   }
   ```

## Available Tools

### 1. `add_todo`
Create a new todo item.

**Parameters:**
- `title` (required): Title of the todo item
- `description` (optional): Detailed description
- `due_date` (optional): Due date in ISO format (e.g., "2024-12-31T23:59:59")
- `priority` (optional): Priority level ("low", "medium", "high")

### 2. `get_all_todos`
Retrieve all todo items with formatted display.

**Parameters:** None

### 3. `update_todo`
Update an existing todo item.

**Parameters:**
- `todo_id` (required): ID of the todo item to update
- `title` (optional): New title
- `description` (optional): New description
- `completed` (optional): Completion status (true/false)
- `due_date` (optional): New due date in ISO format
- `priority` (optional): New priority level

### 4. `delete_todo`
Delete a todo item by ID.

**Parameters:**
- `todo_id` (required): ID of the todo item to delete

### 5. `toggle_todo_status`
Toggle the completion status of a todo item.

**Parameters:**
- `todo_id` (required): ID of the todo item to toggle

## Testing

Run the test script to verify the server works correctly:

```bash
python test_startup.py
```

This will test:
- Database initialization in memory mode
- Creating a todo item
- Retrieving todo items
- Basic functionality verification

## Development

### Project Structure
```
todo-mcp-server/
├── src/
│   └── todo_mcp_server/
│       ├── __init__.py
│       ├── server.py          # Main MCP server implementation
│       ├── database.py        # Database operations and connection handling
│       └── models.py          # Pydantic data models
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── test_startup.py           # Test script
└── README.md                 # This file
```

### Running the Server Directly
```bash
# Activate virtual environment
source venv/bin/activate

# Run with in-memory storage
USE_MEMORY_DB=true python -m src.todo_mcp_server.server

# Run with MongoDB (requires MONGODB_URI)
MONGODB_URI="your-connection-string" python -m src.todo_mcp_server.server
```

## Error Handling

The server includes robust error handling:

- **Database Connection Failures**: Automatically falls back to in-memory storage
- **Invalid Todo IDs**: Returns appropriate error messages
- **Missing Required Parameters**: Validates input and provides clear error messages
- **MongoDB Timeouts**: 5-second timeout with graceful fallback

## MongoDB Setup (Optional)

If you want to use MongoDB persistence:

1. **Create a free MongoDB Atlas account** at https://www.mongodb.com/atlas
2. **Create a new cluster** (free tier available)
3. **Create a database user** with read/write permissions
4. **Get your connection string** from the Atlas dashboard
5. **Update your MCP settings** with the connection string

## Troubleshooting

### Server Won't Start
- Check that the virtual environment is activated
- Verify Python path in MCP settings
- Check for any syntax errors in the configuration

### Database Connection Issues
- Verify MongoDB URI format
- Check network connectivity
- Ensure database user has proper permissions
- The server will automatically fall back to in-memory storage if MongoDB is unavailable

### Tool Execution Errors
- Check that todo IDs are valid ObjectId strings
- Verify required parameters are provided
- Check server logs for detailed error messages

## License

This project is open source and available under the MIT License.