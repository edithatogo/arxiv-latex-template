# arXiv Submission Contract Workflow

This workflow keeps repo-local readiness separate from external arXiv
submission.

## Local Gates

1. `make manuscript-pdf`
2. `make arxiv-upload-ready`
3. `make arxiv-strict-review`
4. `make test`

## Review Roles

- `manuscript_editor`: checks argument structure, claims, declarations, and
  citations.
- `arxiv_toolchain_reviewer`: checks source package, PDF build, and privacy
  audit behavior.
- `publisher_submission_manager`: checks the tarball, manifest, checksums, and
  post-submission record.

## External Gates

Do not mark a manuscript as externally submitted until:

- the upload tarball has been uploaded through the arXiv UI;
- the arXiv-rendered PDF has been inspected and approved;
- the assigned arXiv identifier and version are recorded;
- the uploaded tarball SHA-256 and manifest SHA-256 are recorded.

