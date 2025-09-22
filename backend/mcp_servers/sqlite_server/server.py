#!/usr/bin/env python3
"""
SQLite MCP Server - Learning Implementation (Fixed)
A custom MCP server using FastMCP for local SQLite database operations.
"""

import asyncio
import sqlite3
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP
import mcp.types as types


class SQLiteMCPServer:
    def __init__(self, db_path: str = "project_data.db"):
        self.app = FastMCP("sqlite-tracker")
        self.db_path = Path(db_path).absolute()
        self.setup_database()
        self.setup_tools()
        self.setup_resources()
    
    def setup_database(self):
        """Initialize SQLite database with project tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for project tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                week INTEGER NOT NULL,
                day INTEGER NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'In Progress',
                time_minutes INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                status_code INTEGER,
                response_time_ms FLOAT,
                success BOOLEAN,
                notes TEXT,
                tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def setup_tools(self):
        """Register MCP tools using FastMCP"""
        
        @self.app.tool()
        async def execute_query(query: str, params: str = "[]") -> Dict[str, Any]:
            """Execute a SELECT query and return results"""
            try:
                params_list = json.loads(params) if params else []
                
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.cursor()
                
                cursor.execute(query, params_list)
                
                if query.strip().upper().startswith('SELECT'):
                    rows = cursor.fetchall()
                    result = [dict(row) for row in rows]
                else:
                    conn.commit()
                    result = {"affected_rows": cursor.rowcount}
                
                conn.close()
                
                return {
                    "success": True,
                    "data": result,
                    "message": f"Query executed successfully"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Query execution failed"
                }
        
        @self.app.tool()
        async def log_progress(date: str, week: int, day: int, task: str, 
                             status: str = "In Progress", time_minutes: int = 0, 
                             notes: str = "") -> Dict[str, Any]:
            """Log project progress to database"""
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO project_progress 
                    (date, week, day, task, status, time_minutes, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (date, week, day, task, status, time_minutes, notes))
                
                conn.commit()
                entry_id = cursor.lastrowid
                conn.close()
                
                return {
                    "success": True,
                    "id": entry_id,
                    "message": f"Progress logged for {task}"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to log progress"
                }
        
        @self.app.tool()
        async def add_learning_note(topic: str, content: str, tags: str = "") -> Dict[str, Any]:
            """Add a learning note to the database"""
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO learning_notes (topic, content, tags)
                    VALUES (?, ?, ?)
                """, (topic, content, tags))
                
                conn.commit()
                entry_id = cursor.lastrowid
                conn.close()
                
                return {
                    "success": True,
                    "id": entry_id,
                    "message": f"Learning note added for {topic}"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to add learning note"
                }
        
        @self.app.tool()
        async def test_api_endpoint(endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
            """Test an API endpoint and log results"""
            import time
            import requests
            
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                success = response.status_code == expected_status
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO api_tests 
                    (endpoint, status_code, response_time_ms, success, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (endpoint, response.status_code, response_time, success, 
                     f"Response time: {response_time:.2f}ms"))
                
                conn.commit()
                test_id = cursor.lastrowid
                conn.close()
                
                return {
                    "success": success,
                    "test_id": test_id,
                    "status_code": response.status_code,
                    "response_time_ms": response_time,
                    "message": f"API test {'passed' if success else 'failed'}"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "API test failed"
                }
        
        @self.app.tool()
        async def get_recent_progress(limit: int = 10) -> Dict[str, Any]:
            """Get recent project progress entries"""
            try:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM project_progress 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                conn.close()
                
                return {
                    "success": True,
                    "data": result,
                    "message": f"Retrieved {len(result)} recent progress entries"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to retrieve progress"
                }
    
    def setup_resources(self):
        """Register MCP resources using FastMCP"""
        
        @self.app.resource("schema://project_progress")
        async def get_progress_schema() -> str:
            """Get the schema for project_progress table"""
            return """
            Table: project_progress
            Columns:
            - id: INTEGER PRIMARY KEY
            - date: TEXT (format: YYYY-MM-DD)  
            - week: INTEGER (project week number)
            - day: INTEGER (day within week)
            - task: TEXT (task description)
            - status: TEXT (In Progress, Completed, Blocked)
            - time_minutes: INTEGER (time spent)
            - notes: TEXT (additional notes)
            - created_at: TIMESTAMP (auto)
            """
        
        @self.app.resource("schema://learning_notes")
        async def get_notes_schema() -> str:
            """Get the schema for learning_notes table"""
            return """
            Table: learning_notes
            Columns:
            - id: INTEGER PRIMARY KEY
            - topic: TEXT (learning topic)
            - content: TEXT (note content)
            - tags: TEXT (comma-separated tags)
            - created_at: TIMESTAMP (auto)
            """
    
    async def run(self):
        """Run the MCP server using FastMCP"""
        await self.app.run_stdio_async()


def main():
    """Main entry point for the SQLite MCP server"""
    server = SQLiteMCPServer()
    
    # Run the server
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
