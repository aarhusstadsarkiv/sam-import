import csv
import json
from pathlib import Path

from sam_import.generate import handle_folder


def test_full_functionality(tmp_path: Path) -> None:
    test_file = tmp_path / "test.txt"
    test_file.write_text("hej jeg er en test")

    submission = tmp_path / "submission.json"
    submission_data = {
        "creator": "Simon Glob",
        "dates": "2026",
        "description": "Direkte fra kontoret.",
        "location": "Aarhus Stadsarkiv",
        "terms_accepted": "1",
        "email": "simgl@aarhus.dk",
        "navn": "Simon Glob",
        "files": [
            {
                "mime_type": "text/plain",
                "size": "19",
                "filename": "test.txt",
                "checksum": "sha256:0a8c51a70b03f7b16652de18c13286ab9c0a5fae129bff61cfa7f6f7dc814699",
            }
        ],
    }
    submission.write_text(json.dumps(submission_data))

    handle_folder(tmp_path)

    # Assert all generated files are present
    metadata = tmp_path / "metadata.csv"
    assert metadata.exists()
    assert (tmp_path / "ophavsret.pdf").exists()
    assert (tmp_path / "_regnote.txt").exists()

    # Ensure that the metadata has all the correct fieldnames
    with open(metadata) as file:
        reader = csv.DictReader(file)

        required_fieldnames = (
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
        )

        assert reader.fieldnames is not None
        assert all(name in reader.fieldnames for name in required_fieldnames)

        # Ensure that all CSV fields match the amount of files registered
        count = 0
        for _ in reader:
            count += 1

        assert count == len(submission_data["files"])
