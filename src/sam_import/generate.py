import csv
import json
from hashlib import md5
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

REGNOTE_TEMPLATE = """
navn: {navn}
telefon: {telefon}
email: {email}
"""

ENVIRONMENT = Environment(loader=FileSystemLoader("./src/resources"))
TEMPLATE = ENVIRONMENT.get_template("template.html")


def generate_copyright_pdf(data: dict[str, Any], target: Path) -> None:
    html = TEMPLATE.render(data=data)

    HTML(string=html).write_pdf(target=target)


def handle_folder(dir_path: Path) -> None:
    # Ensure submission.json exists
    submission = dir_path / "submission.json"

    if not submission.exists():
        print(f"Submission file not found in {dir_path}")
        return

    data = json.loads(submission.read_bytes())

    if "telefon" not in data:
        data["telefon"] = ""
        print("Warning: Telefon number is not present in submission.json")

    if "email" not in data:
        data["email"] = ""
        print("Warning: Email is not present in submission.json")

    regnote = dir_path / "_regnote.txt"
    regnote_content = REGNOTE_TEMPLATE.format(
        navn=data["navn"],
        telefon=data["telefon"],
        email=data["email"],
    )
    regnote.write_text(regnote_content.strip())

    with open(dir_path / "metadata.csv", mode="w+") as csv_file:
        fieldnames = [
            "smartarkiveringsid",
            "creator",
            "description",
            "dates",
            "location",
            "mime_type",
            "size",
            "filename",
            "sha256checksum",
            "md5checksum",
        ]
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()

        for file_data in data["files"]:
            filename: str = file_data["filename"]
            file = dir_path / filename

            if not file.exists():
                print(f"{filename} was not found in the folder")
                continue

            md5checksum = md5(file.read_bytes()).hexdigest()

            writer.writerow(
                {
                    "smartarkiveringsid": dir_path.name,
                    "creator": data["creator"],
                    "description": data["description"],
                    "dates": data["dates"] if "dates" in data else "",
                    "location": data["location"] if "location" in data else "",
                    "mime_type": file_data["mime_type"],
                    "size": file_data["size"],
                    "filename": filename,
                    "sha256checksum": file_data["checksum"][7:],  # removes - sha256:
                    "md5checksum": md5checksum,
                }
            )

    generate_copyright_pdf(data, dir_path / "ophavsret.pdf")

    print(
        f"Successfully generated '_regnote.txt', 'metadata.csv' and 'opretshav.pdf' for {dir_path.name}"
    )
