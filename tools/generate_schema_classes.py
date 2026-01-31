#!/usr/bin/env python3
"""
Download XSD schemas and generate Python dataclasses using xsdata.

Usage:
    python tools/generate_schema_classes.py

The generated classes can be imported as :

from ib_edavki.generated.doh_div_3 import doh_div




"""

import subprocess
import sys
from pathlib import Path

XSD_URI = [
    "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
    "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd",
    "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd",
]
# XSLT_URLS = [
#    "https://edavki.durs.si/Documents/Transforms/Doh_Div_3.14-display-sl.xslt",
#    "https://edavki.durs.si/Documents/Transforms/Doh_KDVP_9.22-display-sl.xslt",
# ]

# Directories
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SCHEMAS_DIR = PROJECT_ROOT / "ib_edavki" / "schemas"
OUTPUT_DIR = PROJECT_ROOT / "ib_edavki" / "generated"


def list_local_schemas() -> list[Path]:
    """List local XSD files in the schemas directory."""
    return list(SCHEMAS_DIR.glob("*.xsd"))


def generate_classes(schema_uris: list[str]) -> None:
    """Generate Python classes from XSD files using xsdata."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for schema_uri in schema_uris:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "xsdata",
                "generate",
                str(schema_uri),
                "--package",
                "ib_edavki.generated",
                "--unsafe-hash",
                "-ds",
                "NumPy",
            ],
            cwd=PROJECT_ROOT,
            stdout=sys.stderr,
            stderr=sys.stderr,
        )


def main() -> None:
    xsd_sources = XSD_URI + list_local_schemas()

    if not xsd_sources:
        print(
            "No XSD sources configured. Add URLs to the XSD_URI list.", file=sys.stderr
        )
        sys.exit(1)

    generate_classes(xsd_sources)


if __name__ == "__main__":
    main()
