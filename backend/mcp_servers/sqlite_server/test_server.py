#!/usr/bin/env python3
"""
Test script for SQLite MCP Server
Run this to verify the server works before connecting to Claude Desktop
"""

import asyncio
import sqlite3
import sys
from pathlib import Path

# Add the server directory to Python path
sys.path.append(str(Path(__file__).parent))

from server import SQLiteMCPServer


async def test_server():
    """Test the SQLite MCP server functionality"""
    print("🧪 Testing SQLite MCP Server...")
    
    # Initialize server
    server = SQLiteMCPServer("test_project.db")
    print("✅ FastMCP Server initialized")
    
    # Test database connection
    try:
        conn = sqlite3.connect(server.db_path)
        cursor = conn.cursor()
        
        # Test table creation
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Database tables created: {[t[0] for t in tables]}")
        
        # Test basic insert
        cursor.execute("""
            INSERT INTO project_progress 
            (date, week, day, task, status, time_minutes, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("2025-09-22", 2, 2, "Test SQLite MCP Server", "Testing", 30, "Local test"))
        
        conn.commit()
        print("✅ Test data inserted")
        
        # Test basic query
        cursor.execute("SELECT * FROM project_progress ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        print(f"✅ Test data retrieved: {row}")
        
        conn.close()
        
        # Clean up test database
        Path("test_project.db").unlink(missing_ok=True)
        print("✅ Test database cleaned up")
        
        print("\n🎉 SQLite MCP Server test PASSED!")
        print("\nNext steps:")
        print("1. Install MCP in Python environment: pip install mcp")
        print("2. Add server config to Claude Desktop")
        print("3. Test MCP integration with Claude")
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False
    
    return True


def main():
    """Run the test"""
    print("SQLite MCP Server - Local Test")
    print("=" * 40)
    
    try:
        result = asyncio.run(test_server())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
