from bs4 import BeautifulSoup
import requests


def _clean_text(text):
    lines = (line.strip() for line in text.splitlines())
    parts = (line for line in lines if line)
    return "\n".join(parts)


def load_job_from_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return _clean_text(file.read())


def load_job_from_url(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return _clean_text(soup.get_text(separator="\n"))
