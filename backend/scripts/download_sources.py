#!/usr/bin/env python3
"""Re-download DPDP legal source PDFs listed in manifest.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

SOURCES_DIR = Path(__file__).resolve().parents[1] / "data" / "sources"


def main() -> None:
    manifest_path = SOURCES_DIR / "manifest.json"
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    for item in manifest["sources"]:
        dest = SOURCES_DIR / item["filename"]
        url = item["official_url"]
        print(f"Downloading {item['id']} -> {dest.name}")
        result = subprocess.run(
            [
                "curl", "-fsSL",
                "-A", UA,
                "-H", "Accept: application/pdf,*/*",
                "-o", str(dest),
                url,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  FAILED: {result.stderr.strip()}", file=sys.stderr)
        else:
            print(f"  OK ({dest.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
