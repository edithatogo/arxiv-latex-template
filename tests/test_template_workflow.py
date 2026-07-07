import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_citation_check_passes():
    result = run_script("scripts/check_manuscript_citations.py", "--json")
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["citation_count"] == 2


def test_source_package_and_privacy_audit():
    run_script("scripts/build_arxiv_source_package.py")
    run_script("scripts/clean_arxiv_source_package.py")
    run_script("scripts/audit_arxiv_source_privacy.py")
    audit = json.loads((ROOT / "paper/arxiv-source-privacy-audit.json").read_text(encoding="utf-8"))
    assert audit["status"] == "pass"


def test_upload_ready_manifest():
    run_script("scripts/build_arxiv_source_package.py")
    run_script("scripts/clean_arxiv_source_package.py")
    run_script("scripts/audit_arxiv_source_privacy.py")
    run_script("scripts/build_arxiv_upload_ready.py", "--require-privacy-audit")
    manifest = json.loads((ROOT / "dist/arxiv/arxiv-submission-manifest.json").read_text(encoding="utf-8"))
    assert manifest["archive_sha256"]
    assert (ROOT / "dist/arxiv/SHA256SUMS").exists()

