# PDF Heading Extraction Logic

This project extracts headings and outlines from PDF documents using a set of robust, configurable rules. The logic is implemented in `main.py` and produces a single output file: `output.json`.

## How It Works

### 1. PDF Loading and Text Extraction

- The script loads a PDF using PyMuPDF (`fitz`).
- It extracts all text lines from each page, capturing metadata such as font, size, boldness, position, and page number.
- Only complete, standalone text lines are considered (not table/data fragments).

### 2. Heading Detection Rules

A line is considered a heading if **the entire line** satisfies at least one of the following:

- **Font size is greater than the most frequent (body) font size.**
- **All text is bold.**
- **The line starts with hierarchical numbering** (e.g., `1.1`, `2.3.4`).

**Additional filter:**

- If a line ends with ":", "-", or similar punctuation (en dash, em dash, bullet, etc.), it is **not** considered a heading.

### 3. Merging Consecutive Headings

- Consecutive headings with the same properties (font, size, bold, and page) are merged into a single heading, concatenating their text.

### 4. Title Extraction

- The **first detected heading** is treated as the document title and is **not** included in the outline.

### 5. Heading Level Assignment

- The script maintains a stack of font sizes for heading levels.
- **If there are consecutive headings with no non-heading lines in between, all are assigned H1.**
- For other headings:
  - If the font size is the same as the previous heading, the level stays the same.
  - If the font size decreases, the level increments (deeper, e.g., H1→H2→H3), but never below H3. The new size is pushed onto the stack.
  - If the font size increases, the stack is searched for a matching previous size. If found, the level resets to that level (H1, H2, or H3). If not found, it resets to H1 and the stack is reset.

### 6. Output File

- **output.json**: Contains the document title and an outline array of headings with their levels and page numbers.
  ```json
  {
    "title": "Document Title",
    "outline": [
      { "level": "H1", "text": "Section 1", "page": 2 },
      { "level": "H2", "text": "Subsection 1.1", "page": 3 },
      ...
    ]
  }
  ```

## Usage

### Running with Docker

1. Build the Docker image:

```sh
docker build --platform linux/amd64 -t pdf-processor .
```

2. Run the container (Windows PowerShell):

```sh
docker run --rm -v ${PWD}/sample_dataset/pdfs:/app/input:ro -v ${PWD}/sample_dataset/outputs:/app/output --network none pdf-processor
```

### Running directly with Python

Run the script from the command line:

```sh
python main.py --pdf path/to/your.pdf --output output.json
```

## Customization

- You can adjust the heading detection rules, forbidden line endings, or level assignment logic in `main.py` and the `tools` modules as needed for your documents.

## Requirements

- Python 3.x
- PyMuPDF (`fitz`)

Install dependencies:

```sh
pip install -r requirements.txt
```

---

For questions or further customization, see the comments in `main.py` or contact the author.
