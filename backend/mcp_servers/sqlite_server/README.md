# SQLite MCP Server

A custom Model Context Protocol (MCP) server for local SQLite database operations. This server demonstrates MCP architecture patterns and provides project tracking capabilities.

## Architecture Overview

### MCP Components Built:
- **Tools**: Functions Claude can call (execute_query, log_progress, etc.)
- **Resources**: Data Claude can read (database schemas)
- **Server**: Async communication handler

### Database Schema:
- `project_progress`: Track development tasks and time
- `learning_notes`: Store learning insights and notes  
- `api_tests`: Log API endpoint testing results

## Tools Available:

### Core Database Operations:
- `execute_query(query, params)` - Execute SELECT/INSERT/UPDATE queries
- `log_progress(date, week, day, task, status, time_minutes, notes)` - Log project progress
- `get_recent_progress(limit)` - Retrieve recent progress entries

### Learning & Testing:
- `add_learning_note(topic, content, tags)` - Add learning insights
- `test_api_endpoint(endpoint, expected_status)` - Test and log API calls

## Resources Available:
- `schema://project_progress` - Database schema documentation
- `schema://learning_notes` - Learning notes table schema

## Files:
- `server.py` - Main MCP server implementation
- `test_server.py` - Local testing script
- `claude_config.json` - Claude Desktop MCP configuration
- `requirements.txt` - Python dependencies

## Usage:

### 1. Local Testing:
```bash
python test_server.py
```

### 2. Claude Desktop Integration:
Add the configuration from `claude_config.json` to your Claude Desktop MCP settings.

### 3. Example Claude Interactions:
```
# Log today's progress
Can you log that I completed "Build SQLite MCP Server" for Week 2, Day 2, taking 30 minutes?

# Query recent progress  
Show me my last 5 progress entries

# Add a learning note
Add a learning note about "MCP Architecture" with the content "MCP servers use async tools and resources pattern"
```

## Learning Outcomes:
- ✅ MCP server architecture (tools, resources, server)
- ✅ Async Python patterns for MCP
- ✅ SQLite integration with MCP
- ✅ Tool registration and error handling
- ✅ Resource management for documentation

This server serves as the foundation for more complex MCP servers like our upcoming Crypto Data MCP server.
