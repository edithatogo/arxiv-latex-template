import argparse
import os
import shutil
import subprocess
from pathlib import Path

from config import PAPER_TEX, TMP_DIR


def find_engine() -> list[str] | None:
    env_tectonic = os.environ.get("TECTONIC")
    if env_tectonic and Path(env_tectonic).exists():
        return [env_tectonic]
    tectonic = shutil.which("tectonic")
    if tectonic:
        return [tectonic]
    bundled = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "latex" / "0.2.4" / "bin" / "tectonic.exe"
    if bundled.exists():
        return [str(bundled)]
    latexmk = shutil.which("latexmk")
    if latexmk:
        return [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error"]
    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        return [pdflatex, "-interaction=nonstopmode", "-halt-on-error"]
    return None


def build_pdf(output_dir: Path, require_pdf: bool = False) -> Path:
    engine = find_engine()
    if not engine:
        raise SystemExit("No TeX engine found. Install tectonic, latexmk, or pdflatex.")
    output_dir.mkdir(parents=True, exist_ok=True)
    command = engine + [str(PAPER_TEX)]
    if Path(engine[0]).name.lower().startswith("tectonic"):
        command = engine + ["--outdir", str(output_dir), str(PAPER_TEX)]
    elif "latexmk" in Path(engine[0]).name.lower():
        command = engine + [f"-outdir={output_dir}", str(PAPER_TEX)]
    else:
        command = engine + [f"-output-directory={output_dir}", str(PAPER_TEX)]
    subprocess.run(command, check=True)
    pdf = output_dir / "paper.pdf"
    if require_pdf and not pdf.exists():
        raise SystemExit(f"Expected PDF was not created: {pdf}")
    print(f"Manuscript PDF built with {engine[0]}: {pdf}")
    return pdf


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the manuscript PDF.")
    parser.add_argument("--output-dir", default=str(TMP_DIR / "manuscript-build"))
    parser.add_argument("--require-pdf", action="store_true")
    args = parser.parse_args()
    build_pdf(Path(args.output_dir), args.require_pdf)


if __name__ == "__main__":
    main()
