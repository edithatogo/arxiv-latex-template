# arXiv Submission Process

1. Run `make arxiv-upload-ready` from a clean commit.
2. Confirm `dist/arxiv/arxiv-submission-manifest.json` records the intended
   commit and artifact.
3. Upload `dist/arxiv/uogto-style-arxiv-source.tar.gz` through the arXiv UI.
4. Inspect the arXiv-rendered PDF before final approval.
5. Copy `docs/arxiv-post-submission-record-template.md` into the project
   release notes or submission record and replace every `TODO`.
6. Update `docs/arxiv-submission-state.md`.

The template does not submit to arXiv automatically.

