#!/usr/bin/env python3
"""Simple script to view database contents"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "project_data.db"

print(f"Reading from: {db_path}")
print("=" * 80)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Show all tables
print("\n📊 TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"  - {table['name']}")

# Show project_progress data
print("\n📝 PROJECT PROGRESS:")
print("-" * 80)
cursor.execute("SELECT * FROM project_progress ORDER BY created_at DESC")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(f"\nID: {row['id']}")
        print(f"Date: {row['date']} (Week {row['week']}, Day {row['day']})")
        print(f"Task: {row['task']}")
        print(f"Status: {row['status']}")
        print(f"Time: {row['time_minutes']} minutes")
        print(f"Notes: {row['notes']}")
        print(f"Created: {row['created_at']}")
        print("-" * 80)
else:
    print("No records found")

conn.close()
