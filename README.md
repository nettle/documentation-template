Documentation Template
======================

A lightweight template for writing technical documentation in Markdown,  
rendered as a web site with Docsify and exportable to DOCX and PDF.


Directory Structure
-------------------

```
documentation-template/
├── docs/                           Documentation content
│   ├── index.html                  Docsify entry point
│   ├── index.md                    Landing page
│   ├── sidebar.md                  Navigation and page order
│   └── system-design/              Example document
│       ├── main.md
│       ├── goals.md
│       ├── use-cases.md
│       ├── requirements.md
│       ├── modules.md
│       ├── repo.md
│       ├── development.md
│       └── deployment.md
├── tools/                          Build scripts
│   ├── build-docx.py               Markdown → DOCX
│   ├── build-pdf.py                Markdown → PDF (via pandoc)
│   └── reference.docx              DOCX template (styles, margins)
├── Makefile                        Build targets
├── pyproject.toml                  Python dependencies (UV)
└── README.md                       This file
```


How It Works
------------

1. Write documentation in Markdown under `docs/`
2. Define page order in `docs/sidebar.md`
3. Browse live in a browser via Docsify (no build step)
4. Export to DOCX or PDF, use `make docx` / `make pdf`

NOTE: The build scripts read `sidebar.md` to determine file order,
render Mermaid diagrams to images, and produce a single output file.


Dependencies
------------

- UV Python package manager: https://github.com/astral-sh/uv
- Python 3.10+

Dependencies managed by UV:
- `python-docx` - DOCX generation
- `pypandoc-binary` - PDF generation (bundles pandoc)
- `mermaidx` - Mermaid diagram rendering

System dependency (optional):
- `graphviz` - for Graphviz/DOT diagrams (falls back to code block if not installed)
