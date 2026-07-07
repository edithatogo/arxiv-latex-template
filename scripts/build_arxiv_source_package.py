import json
import shutil
from pathlib import Path

from config import ARXIV_SOURCE_DIR, PAPER_DIR, PAPER_TEX


KEEP_SUFFIXES = {".tex", ".bib", ".bbl", ".cls", ".sty", ".pdf", ".png", ".jpg", ".jpeg"}


def copy_if_exists(source: Path, target: Path) -> bool:
    if not source.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return True


def build_source_package() -> dict:
    if ARXIV_SOURCE_DIR.exists():
        shutil.rmtree(ARXIV_SOURCE_DIR)
    ARXIV_SOURCE_DIR.mkdir(parents=True)
    kept = []
    copy_if_exists(PAPER_TEX, ARXIV_SOURCE_DIR / "paper.tex")
    kept.append("paper.tex")
    figures_dir = PAPER_DIR / "figures"
    if figures_dir.exists():
        for source in figures_dir.rglob("*"):
            if source.is_file() and source.suffix.lower() in KEEP_SUFFIXES:
                rel = source.relative_to(PAPER_DIR)
                copy_if_exists(source, ARXIV_SOURCE_DIR / rel)
                kept.append(rel.as_posix())
    manifest = {
        "schema": "arxiv-template.source-package.v1",
        "package_dir": ".",
        "kept_count": len(kept),
        "kept_files": sorted(kept),
    }
    (ARXIV_SOURCE_DIR / "source-package-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built arXiv source package in {ARXIV_SOURCE_DIR}: kept {len(kept)} files.")
    return manifest


if __name__ == "__main__":
    build_source_package()
