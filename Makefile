PYTHON ?= $(firstword $(wildcard .pixi/envs/default/python.exe .pixi/envs/default/bin/python ../UOGTO/.pixi/envs/default/python.exe ../UOGTO/.pixi/envs/default/bin/python $(USERPROFILE)/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe) python)
ARXIV_PDF_FLAGS ?= --require-pdf
ARXIV_PDF_OUTPUT_DIR ?= .tmp/manuscript-build-arxiv

.PHONY: manuscript-check manuscript-pdf arxiv-source-package arxiv-source-clean arxiv-privacy-audit arxiv-preflight arxiv-upload-ready arxiv-strict-review required-gate test clean

manuscript-check:
	$(PYTHON) scripts/check_manuscript_citations.py

manuscript-pdf: manuscript-check
	$(PYTHON) scripts/build_manuscript_pdf.py --require-pdf

arxiv-source-package: manuscript-check
	$(PYTHON) scripts/build_arxiv_source_package.py

arxiv-source-clean: arxiv-source-package
	$(PYTHON) scripts/clean_arxiv_source_package.py

arxiv-privacy-audit: arxiv-source-clean
	$(PYTHON) scripts/audit_arxiv_source_privacy.py

arxiv-preflight: manuscript-check
	$(PYTHON) scripts/build_manuscript_pdf.py --output-dir $(ARXIV_PDF_OUTPUT_DIR) $(ARXIV_PDF_FLAGS)
	$(PYTHON) scripts/build_arxiv_source_package.py
	$(PYTHON) scripts/clean_arxiv_source_package.py
	$(PYTHON) scripts/audit_arxiv_source_privacy.py

arxiv-upload-ready: arxiv-preflight
	$(PYTHON) scripts/build_arxiv_upload_ready.py --require-privacy-audit

arxiv-strict-review:
	$(PYTHON) scripts/score_arxiv_submission.py --threshold 900

required-gate: manuscript-pdf arxiv-upload-ready arxiv-strict-review test

test:
	$(PYTHON) -m pytest

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('.tmp'), pathlib.Path('dist')]]"
