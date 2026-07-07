import json
from pathlib import Path

from config import ARXIV_SOURCE_DIR


REMOVE_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
}


def is_safe_name(path: Path) -> bool:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/")
    return all(char in allowed for char in path.as_posix())


def clean_package() -> dict:
    removed = []
    unsafe = []
    if not ARXIV_SOURCE_DIR.exists():
        raise SystemExit("Build the arXiv source package first.")
    for path in ARXIV_SOURCE_DIR.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ARXIV_SOURCE_DIR)
        if not is_safe_name(rel):
            unsafe.append(rel.as_posix())
        lower_name = path.name.lower()
        if path.suffix.lower() in REMOVE_SUFFIXES or lower_name.endswith(".synctex.gz"):
            path.unlink()
            removed.append(rel.as_posix())
    if unsafe:
        raise SystemExit("Unsafe arXiv filenames: " + ", ".join(unsafe))
    kept = sorted(path.relative_to(ARXIV_SOURCE_DIR).as_posix() for path in ARXIV_SOURCE_DIR.rglob("*") if path.is_file())
    manifest = {"removed_count": len(removed), "removed_files": sorted(removed), "kept_count": len(kept), "kept_files": kept}
    (ARXIV_SOURCE_DIR / "clean-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Cleaned arXiv source package: removed {len(removed)} files, kept {len(kept)} files.")
    return manifest


if __name__ == "__main__":
    clean_package()

