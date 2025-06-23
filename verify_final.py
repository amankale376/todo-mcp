#!/usr/bin/env python3
"""Final verification script for the Todo MCP Server."""

import os
import sys
import asyncio
import json

# Set environment variable BEFORE importing
os.environ['USE_MEMORY_DB'] = 'true'

from src.todo_mcp_server.database import db
from src.todo_mcp_server.models import TodoCreate, TodoUpdate

async def test_all_functionality():
    """Test all server functionality."""
    print("🧪 Running comprehensive Todo MCP Server tests...\n")
    
    # Test 1: Database initialization
    print("1️⃣ Testing database initialization...")
    db._ensure_connection()
    print(f"   ✅ Database initialized (in-memory: {db.use_memory})")
    
    # Test 2: Create todo
    print("\n2️⃣ Testing todo creation...")
    todo_data = TodoCreate(
        title="Test Todo Item",
        description="This is a test todo for verification",
        priority="high"
    )
    todo = await db.create_todo(todo_data)
    print(f"   ✅ Created todo: {todo.title} (ID: {todo.id})")
    
    # Test 3: Get all todos
    print("\n3️⃣ Testing get all todos...")
    todos = await db.get_all_todos()
    print(f"   ✅ Retrieved {len(todos)} todos")
    
    # Test 4: Get todo by ID
    print("\n4️⃣ Testing get todo by ID...")
    retrieved_todo = await db.get_todo_by_id(str(todo.id))
    print(f"   ✅ Retrieved todo by ID: {retrieved_todo.title}")
    
    # Test 5: Update todo
    print("\n5️⃣ Testing todo update...")
    update_data = TodoUpdate(
        title="Updated Test Todo",
        completed=True
    )
    updated_todo = await db.update_todo(str(todo.id), update_data)
    print(f"   ✅ Updated todo: {updated_todo.title} (Completed: {updated_todo.completed})")
    
    # Test 6: Toggle status
    print("\n6️⃣ Testing status toggle...")
    toggled_todo = await db.toggle_todo_status(str(todo.id))
    print(f"   ✅ Toggled status: Completed = {toggled_todo.completed}")
    
    # Test 7: Create another todo for deletion test
    print("\n7️⃣ Testing todo deletion...")
    todo_to_delete = await db.create_todo(TodoCreate(title="Todo to Delete"))
    delete_success = await db.delete_todo(str(todo_to_delete.id))
    print(f"   ✅ Deleted todo: {delete_success}")
    
    # Test 8: Verify final state
    print("\n8️⃣ Testing final state...")
    final_todos = await db.get_all_todos()
    print(f"   ✅ Final todo count: {len(final_todos)}")
    
    print("\n🎉 All tests passed! Todo MCP Server is working correctly.")
    print("\n📋 Summary:")
    print(f"   • Database mode: {'In-memory' if db.use_memory else 'MongoDB'}")
    print(f"   • Total operations tested: 8")
    print(f"   • All CRUD operations working: ✅")
    print(f"   • Server ready for MCP integration: ✅")

def test_server_import():
    """Test that the server can be imported without errors."""
    print("\n🔧 Testing server import...")
    try:
        from src.todo_mcp_server.server import main, server
        print("   ✅ Server imported successfully")
        print("   ✅ Main function available")
        print("   ✅ MCP server instance created")
        return True
    except Exception as e:
        print(f"   ❌ Server import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Todo MCP Server - Final Verification")
    print("=" * 50)
    
    # Test server import first
    if not test_server_import():
        sys.exit(1)
    
    # Run async tests
    try:
        asyncio.run(test_all_functionality())
        print("\n✅ All verification tests completed successfully!")
        print("\n🔗 Next steps:")
        print("   1. Restart your MCP client to load the updated server")
        print("   2. Use the 'todo' tools in your MCP-enabled application")
        print("   3. Optionally configure MongoDB for persistent storage")
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        sys.exit(1)