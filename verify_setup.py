#!/usr/bin/env python3
"""
Setup verification script for Todo MCP Server
"""

import os
import sys
from dotenv import load_dotenv

def verify_setup():
    """Verify that the setup is correct."""
    print("🔍 Verifying Todo MCP Server setup...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check environment variables
    mongodb_uri = os.getenv("MONGODB_URI")
    mongodb_db = os.getenv("MONGODB_DATABASE", "todo_db")
    
    if mongodb_uri:
        print(f"✅ MONGODB_URI: {mongodb_uri[:30]}...")
        print(f"✅ MONGODB_DATABASE: {mongodb_db}")
    else:
        print("❌ MONGODB_URI not set in environment variables")
        return False
    
    # Check if package is importable
    try:
        import todo_mcp_server
        print(f"✅ Package importable: todo_mcp_server v{todo_mcp_server.__version__}")
    except ImportError as e:
        print(f"❌ Cannot import package: {e}")
        return False
    
    # Check dependencies
    required_packages = ['mcp', 'pymongo', 'pydantic', 'fastapi', 'uvicorn']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            return False
    
    # Test MongoDB connection (optional)
    try:
        from todo_mcp_server.database import db
        print("\n🔗 Testing MongoDB connection...")
        db.connect()
        print("✅ MongoDB connection successful!")
        db.disconnect()
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("   This is expected if you haven't set up your real MongoDB credentials yet.")
        print("   Please update your .env file with your actual MongoDB Atlas connection string.")
    
    print("\n" + "=" * 50)
    print("🎉 Setup verification complete!")
    print("\n📝 Next steps:")
    print("1. Update .env with your real MongoDB Atlas credentials")
    print("2. Run: ./start.sh")
    print("3. The MCP server should be ready to use!")
    
    return True

if __name__ == "__main__":
    verify_setup()