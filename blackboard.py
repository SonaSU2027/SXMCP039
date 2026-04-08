import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# This forces the DB file to be created IN that same folder
DB_NAME = os.path.join(BASE_DIR, "blackboard.db")
# -------------------------------
# INIT DATABASE
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Create the high-level tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY,
        status TEXT
    )
    """)

    # 2. SCHEMA SAFETY CHECK:
    # We check if the 'updates' table exists and if it has the correct column.
    # If the column 'update_json' is missing, we drop the table so it can be recreated.
    try:
        cursor.execute("SELECT update_json FROM updates LIMIT 1")
    except sqlite3.OperationalError:
        # This error triggers if the column 'update_json' does NOT exist.
        print("Old database schema detected. Resetting 'updates' table...")
        cursor.execute("DROP TABLE IF EXISTS updates")

    # 3. Create the structured updates table (The "Bus")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT,
        update_json TEXT 
    )
    """)

    conn.commit()
    conn.close()

# -------------------------------
# WRITE TO BLACKBOARD (The "Push")
# -------------------------------
def write_to_blackboard(task_id, data_dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    json_data = json.dumps(data_dict)

    cursor.execute("""
    INSERT INTO updates (task_id, update_json)
    VALUES (?, ?)
    """, (task_id, json_data))

    cursor.execute("""
    INSERT OR IGNORE INTO tasks (task_id, status)
    VALUES (?, ?)
    """, (task_id, "in_progress"))

    conn.commit()
    conn.close()

# -------------------------------
# READ FROM BLACKBOARD (The "Sync")
# -------------------------------
def read_from_blackboard(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT update_json FROM updates
    WHERE task_id = ?
    ORDER BY id DESC LIMIT 1
    """, (task_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row[0])
    return {}

# -------------------------------
# UPDATE TASK STATUS
# -------------------------------
def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
    conn.commit()
    conn.close()

# -------------------------------
# GET FULL STATE (For Final Demo)
# -------------------------------
def get_full_state(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM tasks WHERE task_id = ?", (task_id,))
    status_row = cursor.fetchone()

    cursor.execute("SELECT update_json FROM updates WHERE task_id = ? ORDER BY id ASC", (task_id,))
    updates = [json.loads(row[0]) for row in cursor.fetchall()]

    conn.close()

    return {
        "task_id": task_id,
        "status": status_row[0] if status_row else "unknown",
        "history": updates
    }