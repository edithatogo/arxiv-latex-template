import argparse
import json
from pathlib import Path

from config import ARXIV_DIST_DIR, PAPER_DIR, PAPER_TEX


def score() -> tuple[int, list[str]]:
    points = 0
    notes = []
    checks = [
        (PAPER_TEX.exists(), 160, "paper source exists"),
        ((PAPER_DIR / "references.csl.json").exists(), 120, "CSL references exist"),
        ((PAPER_DIR / "arxiv-source-privacy-audit.json").exists(), 160, "privacy audit exists"),
        ((ARXIV_DIST_DIR / "arxiv-submission-manifest.json").exists(), 180, "upload manifest exists"),
        ((ARXIV_DIST_DIR / "SHA256SUMS").exists(), 120, "checksums exist"),
        ((ARXIV_DIST_DIR / "00README.json").exists(), 80, "upload README exists"),
    ]
    text = PAPER_TEX.read_text(encoding="utf-8") if PAPER_TEX.exists() else ""
    checks.extend(
        [
            ("\\section{Limitations}" in text, 80, "limitations section exists"),
            ("\\section{Data and code availability}" in text, 50, "data/code availability exists"),
            ("\\section{Declarations}" in text, 50, "declarations section exists"),
        ]
    )
    for ok, value, label in checks:
        if ok:
            points += value
        else:
            notes.append(f"missing: {label}")
    manifest_path = ARXIV_DIST_DIR / "arxiv-submission-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("git", {}).get("dirty"):
            notes.append("warning: manifest records a dirty git tree")
    return points, notes


def main() -> None:
    parser = argparse.ArgumentParser(description="Score arXiv template submission readiness.")
    parser.add_argument("--threshold", type=int, default=900)
    args = parser.parse_args()
    value, notes = score()
    print(f"arXiv template score: {value}/1000")
    for note in notes:
        print(f"- {note}")
    if value < args.threshold:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

