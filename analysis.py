import sqlite3


DB_PATH = "data/jobs.db"


def get_tool_frequencies():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT tools.name, COUNT(job_tools.job_id) AS frequency
        FROM job_tools
        JOIN tools ON tools.id = job_tools.tool_id
        GROUP BY tools.id, tools.name
        ORDER BY frequency DESC, tools.name ASC
        """
    )

    results = cursor.fetchall()
    conn.close()
    return results


def main():
    for tool_name, frequency in get_tool_frequencies():
        print(f"{tool_name}: {frequency}")


if __name__ == "__main__":
    main()
