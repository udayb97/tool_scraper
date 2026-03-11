import sqlite3

DB_PATH = "data/jobs.db"

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        raw_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_tools (
        job_id INTEGER,
        tool_id INTEGER,
        FOREIGN KEY(job_id) REFERENCES jobs(id),
        FOREIGN KEY(tool_id) REFERENCES tools(id)
    )
    """)

    conn.commit()
    conn.close()

def insert_job(url, raw_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jobs (url, raw_text) VALUES (?, ?)",
        (url, raw_text),
    )

    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return job_id

def insert_tool(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO tools (name) VALUES (?)", (name,))
    cursor.execute("SELECT id FROM tools WHERE name = ?", (name,))

    tool_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return tool_id

def link_job_tool(job_id, tool_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO job_tools (job_id, tool_id) VALUES (?, ?)",
        (job_id, tool_id),
    )

    conn.commit()
    conn.close()
