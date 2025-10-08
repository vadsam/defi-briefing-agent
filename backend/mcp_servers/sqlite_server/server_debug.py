#!/usr/bin/env python3
"""
Debug wrapper for SQLite MCP Server - helps diagnose startup issues
"""

import sys
from pathlib import Path

# Log startup to a file so we can see what's happening
log_file = Path(__file__).parent / "startup_log.txt"

try:
    with open(log_file, "w") as f:
        f.write("=== SQLite MCP Server Startup Debug Log ===\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Python path: {sys.executable}\n")
        f.write(f"Working directory: {Path.cwd()}\n\n")
        
        f.write("Attempting to import mcp...\n")
        from mcp.server.fastmcp import FastMCP
        f.write("✓ MCP imported successfully\n\n")
        
        f.write("Importing server module...\n")
        from server import SQLiteMCPServer, main
        f.write("✓ Server module imported successfully\n\n")
        
        f.write("Starting server...\n")
        f.flush()
        
    # Run the actual server
    main()
    
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"\n❌ ERROR: {str(e)}\n")
        f.write(f"Error type: {type(e).__name__}\n")
        import traceback
        f.write(f"Traceback:\n{traceback.format_exc()}")
    
    # Re-raise so Claude Desktop sees the error too
    raise
