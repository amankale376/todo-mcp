# Todo MCP Server

An MCP (Model Context Protocol) server that provides to-do list management functionality with MongoDB backend.

## Features

- **CRUD Operations**: Create, read, update, and delete to-do items
- **Status Management**: Mark items as completed or pending
- **MongoDB Integration**: Persistent storage using MongoDB Atlas or local MongoDB
- **Priority System**: Low, medium, high priority levels with emoji indicators
- **Due Dates**: Optional due date tracking
- **Timestamps**: Automatic creation and update timestamps

## Tools Available

- `add_todo`: Add a new to-do item with title, description, due date, and priority
- `get_all_todos`: Retrieve all to-do items with formatted display
- `update_todo`: Update an existing to-do item
- `delete_todo`: Delete a to-do item
- `toggle_todo_status`: Toggle completion status of a to-do item

## Prerequisites

### MongoDB Setup

You need a MongoDB instance. Choose one of these options:

#### Option 1: MongoDB Atlas (Recommended - Free Tier Available)
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account and cluster
3. Get your connection string from "Connect" → "Connect your application"
4. Whitelist your IP address in Network Access
5. Create a database user in Database Access

#### Option 2: Local MongoDB
```bash
# macOS with Homebrew
brew install mongodb-community
brew services start mongodb-community

# Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongodb

# Docker
docker run -d -p 27017:27017 --name mongodb mongo:7
```

## Setup

### Method 1: Virtual Environment (Recommended)

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
pip install -e .
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your MongoDB connection details
```

5. **Update your .env file:**
```bash
# For MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=todo_db

# For Local MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=todo_db
```

6. **Run the server:**
```bash
./start.sh
# Or manually:
python -m todo_mcp_server.server
```

### Method 2: Docker

1. **Build and run with Docker Compose:**
```bash
# Update .env with your MongoDB URI first
docker-compose up --build
```

2. **Or build and run manually:**
```bash
docker build -t todo-mcp-server .
docker run -e MONGODB_URI="your-connection-string" todo-mcp-server
```

## Configuration

### Environment Variables

- `MONGODB_URI`: MongoDB connection string (required)
- `MONGODB_DATABASE`: Database name (default: "todo_db")
- `ENVIRONMENT`: Set to "development" for verbose logging (optional)

### MCP Server Configuration

Add to your MCP settings file:

```json
{
  "mcpServers": {
    "todo": {
      "command": "python",
      "args": ["-m", "todo_mcp_server.server"],
      "env": {
        "MONGODB_URI": "your-mongodb-connection-string",
        "MONGODB_DATABASE": "todo_db"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Usage

Once configured as an MCP server, you can use the tools to manage your to-do list:

### Adding Todos
- Create items with titles, descriptions, due dates, and priority levels
- Priority levels: low (🟢), medium (🟡), high (🔴)

### Managing Todos
- View all todos with status indicators (✅ completed, ⏳ pending)
- Update any todo properties
- Toggle completion status
- Delete todos you no longer need

### Example Commands
```bash
# Add a high-priority todo with due date
add_todo(title="Complete project", description="Finish the MCP server", priority="high", due_date="2024-01-15T10:00:00")

# Get all todos
get_all_todos()

# Toggle completion status
toggle_todo_status(todo_id="60f7b3b3b3b3b3b3b3b3b3b3")

# Update a todo
update_todo(todo_id="60f7b3b3b3b3b3b3b3b3b3b3", title="Updated title", completed=true)

# Delete a todo
delete_todo(todo_id="60f7b3b3b3b3b3b3b3b3b3b3")
```

## Troubleshooting

### Connection Issues
1. **Check MongoDB URI**: Ensure your connection string is correct
2. **Network Access**: For Atlas, whitelist your IP address
3. **Authentication**: Verify username and password
4. **Firewall**: Ensure port 27017 is accessible (for local MongoDB)

### Common Errors
- `ConnectionError`: MongoDB is not accessible
- `AuthenticationFailed`: Wrong username/password
- `ServerSelectionTimeoutError`: Network connectivity issues

### Logs
The server provides detailed connection logs to help diagnose issues.

## Development

### Project Structure
```
todo-mcp-server/
├── src/todo_mcp_server/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Pydantic data models
│   ├── database.py          # MongoDB operations
│   └── server.py            # MCP server implementation
├── .env                     # Environment variables
├── .env.example             # Environment template
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── start.sh                 # Startup script
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### Transport Type
This MCP server uses **Stdio (Standard Input/Output)** transport, communicating through stdin/stdout streams for reliable local process communication.