from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
PAPER_TEX = PAPER_DIR / "paper.tex"
REFERENCES_CSL = PAPER_DIR / "references.csl.json"
TMP_DIR = ROOT / ".tmp"
DIST_DIR = ROOT / "dist"
ARXIV_SOURCE_DIR = TMP_DIR / "arxiv-source-package"
ARXIV_DIST_DIR = DIST_DIR / "arxiv"
ARCHIVE_BASENAME = "uogto-style-arxiv-source"

