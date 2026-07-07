import json
import re
from pathlib import Path

from config import ARXIV_SOURCE_DIR, PAPER_DIR


PRIVATE_PATTERNS = [
    re.compile(r"[A-Za-z]:[/\\]Users[/\\]", re.IGNORECASE),
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
    re.compile(r"OneDrive\s+-", re.IGNORECASE),
    re.compile(r"BEGIN (?:RSA |OPENSSH |DSA |EC )?PRIVATE KEY"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
]


def scan_text(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings = []
    for pattern in PRIVATE_PATTERNS:
        if pattern.search(text):
            findings.append(pattern.pattern)
    return findings


def audit(source_dir: Path = ARXIV_SOURCE_DIR) -> dict:
    if not source_dir.exists():
        raise SystemExit("Build the arXiv source package first.")
    findings = []
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(source_dir).as_posix()
        if any(part.startswith(".") for part in Path(rel).parts):
            findings.append({"file": rel, "issue": "hidden file in arXiv package"})
        for pattern in scan_text(path):
            findings.append({"file": rel, "issue": "private-pattern", "pattern": pattern})
    result = {
        "schema": "arxiv-template.privacy-audit.v1",
        "status": "pass" if not findings else "fail",
        "finding_count": len(findings),
        "findings": findings,
    }
    output_json = PAPER_DIR / "arxiv-source-privacy-audit.json"
    output_md = PAPER_DIR / "arxiv-source-privacy-audit.md"
    output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(
        "# arXiv Source Privacy Audit\n\n"
        f"Status: `{result['status']}`\n\n"
        f"Findings: `{len(findings)}`\n",
        encoding="utf-8",
    )
    if findings:
        raise SystemExit("arXiv source privacy audit failed.")
    print(f"arXiv source privacy audit pass: {output_json}")
    return result


if __name__ == "__main__":
    audit()

