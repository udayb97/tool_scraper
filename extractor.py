from pathlib import Path
import re

SKILLS_FILE = Path("skills_dictionary.txt")


def load_tool_names(file_path=SKILLS_FILE):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def extract_tools(job_text, file_path=SKILLS_FILE):
    detected_tools = []
    seen = set()
    job_text_lower = job_text.lower()

    tools = load_tool_names(file_path)

    for tool in tools:
        tool_key = tool.lower()
        pattern = r"(?<!\w)" + re.escape(tool_key) + r"(?!\w)"

        if tool_key not in seen and re.search(pattern, job_text_lower):
            detected_tools.append(tool)
            seen.add(tool_key)

    return detected_tools
