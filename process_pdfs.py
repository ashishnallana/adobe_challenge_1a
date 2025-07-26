import os
from pathlib import Path
from tools.pdf_loader import load_pdf_from_path
from tools.text_extraction import extract_text_lines
from tools.heading_detection import detect_headings_and_levels
from tools.io_utils import save_json_output


def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")

    if not input_dir.exists():
        print("Input directory does not exist. Exiting.")
        return

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in input directory.")
        return

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        doc = load_pdf_from_path(pdf_file)
        if not doc:
            print(f"Failed to load: {pdf_file.name}")
            continue

        lines = extract_text_lines(doc)
        title, outline, headings, most_frequent_size = detect_headings_and_levels(
            lines)

        outline_data = {
            "title": title if title else "",
            "outline": outline
        }

        output_file = output_dir / f"{pdf_file.stem}.json"
        save_json_output(outline_data, output_file)
        print(f"Saved: {output_file.name}")


if __name__ == "__main__":
    process_pdfs()
