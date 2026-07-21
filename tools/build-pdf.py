"""Build a PDF document from a documentation directory.

Usage:
    python tools/build-pdf.py docs/system-design

Reads sidebar.md to determine file order, concatenates markdown files,
and produces a single PDF in output/ using pandoc.
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import pypandoc


def parse_sidebar(sidebar_path):
    """Parse sidebar.md and return ordered list of relative markdown paths."""
    files = []
    with open(sidebar_path, "r", encoding="utf-8") as handle:
        for line in handle:
            match = re.search(r"\[.*?\]\((.*?)\)", line)
            if match:
                link = match.group(1)
                if not link or link.startswith("http"):
                    continue
                if not link.endswith(".md"):
                    link += ".md"
                files.append(link)
    return files


def find_sidebar(docs_path):
    """Find sidebar.md in the given directory or its parent."""
    sidebar_path = docs_path / "sidebar.md"
    if sidebar_path.exists():
        return sidebar_path
    parent_sidebar = docs_path.parent / "sidebar.md"
    if parent_sidebar.exists():
        return parent_sidebar
    return None


def build_pdf(docs_dir, output_dir):
    """Build a PDF document from the documentation directory."""
    docs_path = Path(docs_dir)
    sidebar_path = find_sidebar(docs_path)

    if not sidebar_path:
        logging.error("ERROR: sidebar.md not found in %s or its parent", docs_path)
        sys.exit(1)

    # Parse sidebar for file order, resolve relative to sidebar location
    raw_files = parse_sidebar(sidebar_path)
    sidebar_dir = sidebar_path.parent
    file_list = []
    for file_path in raw_files:
        full_path = sidebar_dir / file_path
        if full_path.resolve().is_relative_to(docs_path.resolve()):
            file_list.append(str(full_path.relative_to(docs_path)))

    logging.info("Found %d files in sidebar.md for %s", len(file_list), docs_path.name)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Concatenate all markdown files
    combined_markdown = ""
    for file_path in file_list:
        full_path = docs_path / file_path
        if not full_path.exists():
            logging.warning("WARNING: Skipping %s (not found)", file_path)
            continue
        logging.info("  Processing %s", file_path)
        content = full_path.read_text(encoding="utf-8")
        if content.strip():
            combined_markdown += content + "\n\n"

    # Convert to PDF using pandoc
    output_name = docs_path.name
    output_file = output_path / f"{output_name}.pdf"

    pypandoc.convert_text(
        combined_markdown,
        "pdf",
        format="md",
        outputfile=str(output_file),
        extra_args=["--pdf-engine=pdflatex", "-V", "geometry:margin=2.5cm"],
    )
    logging.info("Saved: %s", output_file)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Build a PDF document from a documentation directory.")
    parser.add_argument(
        "docs_dir",
        help="Path to the documentation directory (e.g., docs/system-design)")
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory (default: output)")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output")
    return parser.parse_args()


def main():
    """Entry point."""
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s")
    build_pdf(args.docs_dir, args.output)


if __name__ == "__main__":
    main()
