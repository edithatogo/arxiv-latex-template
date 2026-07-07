import argparse
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from config import ARCHIVE_BASENAME, ARXIV_DIST_DIR, ARXIV_SOURCE_DIR, PAPER_DIR, ROOT


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_state() -> dict:
    import subprocess

    try:
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return {"available": False}
    dirty_entries = [line for line in status.splitlines() if line.strip()]
    return {
        "available": True,
        "head": head,
        "dirty": bool(dirty_entries),
        "dirty_file_count": len(dirty_entries),
        "dirty_entries": dirty_entries,
    }


def build_upload_ready(require_privacy_audit: bool = False) -> dict:
    if not ARXIV_SOURCE_DIR.exists():
        raise SystemExit("Build and clean the arXiv source package first.")
    audit_path = PAPER_DIR / "arxiv-source-privacy-audit.json"
    if require_privacy_audit:
        if not audit_path.exists():
            raise SystemExit("Privacy audit is required but missing.")
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if audit.get("status") != "pass":
            raise SystemExit("Privacy audit is required but did not pass.")
    ARXIV_DIST_DIR.mkdir(parents=True, exist_ok=True)
    archive = ARXIV_DIST_DIR / f"{ARCHIVE_BASENAME}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for path in sorted(ARXIV_SOURCE_DIR.rglob("*")):
            if path.is_file():
                tar.add(path, arcname=path.relative_to(ARXIV_SOURCE_DIR).as_posix())
    checksums = {archive.name: sha256(archive)}
    (ARXIV_DIST_DIR / "SHA256SUMS").write_text(
        "".join(f"{value}  {name}\n" for name, value in sorted(checksums.items())),
        encoding="utf-8",
    )
    manifest = {
        "schema": "arxiv-template.upload-ready.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "archive": str(archive),
        "archive_sha256": checksums[archive.name],
        "source_file_count": sum(1 for path in ARXIV_SOURCE_DIR.rglob("*") if path.is_file()),
        "git": git_state(),
        "privacy_audit": str(audit_path) if audit_path.exists() else None,
    }
    (ARXIV_DIST_DIR / "arxiv-submission-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (ARXIV_DIST_DIR / "00README.json").write_text(
        json.dumps(
            {
                "upload": archive.name,
                "instruction": "Upload the tar.gz through the arXiv UI, inspect the rendered PDF, then record the assigned identifier.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"arXiv upload-ready archive: {archive}")
    print(f"SHA256: {checksums[archive.name]}")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build arXiv upload-ready tarball and checksums.")
    parser.add_argument("--require-privacy-audit", action="store_true")
    args = parser.parse_args()
    build_upload_ready(args.require_privacy_audit)


if __name__ == "__main__":
    main()
