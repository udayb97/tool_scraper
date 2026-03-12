import argparse

from database import initialize_database, insert_job, insert_tool, link_job_tool
from extractor import extract_tools
from ingestion import load_job_from_text, load_job_from_url


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest a job description and extract tools.")
    
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--text", dest="text_file", help="Path to a text file with a job description")
    source_group.add_argument("--url", dest="job_url", help="URL of a job posting")
    source_group.add_argument("--batch", dest="batch_file", help="File containing multiple job URLs")

    return parser.parse_args()


def main():
    args = parse_args()
    initialize_database()

    # ---- BATCH MODE ----
    if args.batch_file:
        with open(args.batch_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        for url in urls:
            job_text = load_job_from_url(url)
            detected_tools = extract_tools(job_text)
            job_id = insert_job(url, job_text)

            for tool_name in detected_tools:
                tool_id = insert_tool(tool_name)
                link_job_tool(job_id, tool_id)

            print(f"Processed job_id {job_id} from {url}")

        return

    # ---- SINGLE JOB MODE ----
    if args.text_file:
        source_value = args.text_file
        job_text = load_job_from_text(args.text_file)
    else:
        source_value = args.job_url
        job_text = load_job_from_url(args.job_url)

    detected_tools = extract_tools(job_text)

    job_id = insert_job(source_value, job_text)

    for tool_name in detected_tools:
        tool_id = insert_tool(tool_name)
        link_job_tool(job_id, tool_id)

    print(f"job_id: {job_id}")
    print("detected_tools:")

    for tool_name in detected_tools:
        print(f"- {tool_name}")

if __name__ == "__main__":
    main()
