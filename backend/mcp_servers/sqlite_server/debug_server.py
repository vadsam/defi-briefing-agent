#!/usr/bin/env python3
"""
Debug script to understand MCP Server API
"""

from mcp.server import Server

# Create server and check its attributes
server = Server("test")
print("Server methods and attributes:")
print([attr for attr in dir(server) if not attr.startswith('_')])
