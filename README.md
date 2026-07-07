# arXiv LaTeX Template

Reusable arXiv-ready LaTeX article template distilled from the UOGTO manuscript
workflow. It keeps the parts that generalize:

- clean 11pt article layout with restrained color, microtypography, URL wrapping,
  custom title block, compact abstract, glossary and abbreviation anchors;
- deterministic manuscript PDF build;
- citation-key reconciliation against CSL JSON;
- arXiv source package creation and cleaning;
- privacy audit for local paths, credentials, and hidden files;
- upload-ready tarball, manifest, and SHA256 checksums;
- GitHub Actions for PDF build, arXiv preflight, and an aggregate required gate;
- reusable submission-agent and workflow documentation.

## Quick Start

```powershell
make manuscript-pdf
make arxiv-upload-ready
make test
```

The upload bundle is written to `dist/arxiv/uogto-style-arxiv-source.tar.gz` by
default. Rename it for your project in `scripts/config.py`.

## Repository Layout

- `paper/paper.tex`: sample article using the reusable style.
- `paper/references.csl.json`: canonical manuscript references.
- `scripts/`: build, citation, packaging, audit, and scoring utilities.
- `tests/`: focused regression tests for citation and packaging behavior.
- `agents/` and `workflows/`: reusable arXiv submission review contracts.
- `.github/workflows/`: CI workflows for main branches and PRs.

## Adaptation Checklist

1. Replace title, author, metadata, abstract, body, glossary, and references.
2. Update `paper/references.csl.json` with every cited key.
3. Add figures under `paper/figures/` using PDF, PNG, JPG/JPEG, or source-safe
   TikZ.
4. Run `make arxiv-upload-ready`.
5. Inspect `dist/arxiv/arxiv-submission-manifest.json` and `dist/arxiv/SHA256SUMS`.
6. Upload the tarball through the arXiv UI as the registered submitting author.
7. Inspect the arXiv-rendered PDF before final submission.

## Notes

This repository does not claim a paper has been submitted. External arXiv
identifier assignment and rendered-PDF approval remain human submission steps.

