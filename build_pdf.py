"""Render the downloadable PDF CV from the YAML into assets/.

Usage:  python build_pdf.py
Requires:  pip install "rendercv[full]"
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
YAML = ROOT / "Abdelrahman_Ali_CV.yaml"
BUILD = ROOT / "rendercv_output"
DEST = ROOT / "assets" / "Abdelrahman_Ali_CV.pdf"


def main() -> None:
    subprocess.run(
        [sys.executable, "-m", "rendercv", "render", str(YAML), "-o", str(BUILD), "-q"],
        check=True,
        cwd=ROOT,
    )
    DEST.parent.mkdir(exist_ok=True)
    shutil.copy(next(BUILD.glob("*.pdf")), DEST)
    print(f"Wrote {DEST}")


if __name__ == "__main__":
    main()
