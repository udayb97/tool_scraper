from pathlib import Path
import re

SKILLS_FILE = Path("skills_dictionary.txt")


def load_tool_names(file_path=SKILLS_FILE):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def build_tool_regex(tools):
    escaped_tools = [re.escape(tool.lower()) for tool in tools]
    pattern = r"\b(" + "|".join(escaped_tools) + r")\b"
    return re.compile(pattern)


def extract_tools(job_text, file_path=SKILLS_FILE):
    tools = load_tool_names(file_path)

    tool_regex = build_tool_regex(tools)

    job_text_lower = job_text.lower()

    matches = tool_regex.findall(job_text_lower)

    detected = set()

    for match in matches:
        for tool in tools:
            if tool.lower() == match:
                detected.add(tool)

    return sorted(detected)