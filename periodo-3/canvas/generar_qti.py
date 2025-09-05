#!/usr/bin/env python3
"""Simple QTI generator for período-3 using txttoqti v0.5.0 Python API."""

import sys
from pathlib import Path

try:
    import txttoqti
except ImportError:
    print("❌ txttoqti not found. Install with: pip install txttoqti>=0.5.0")
    sys.exit(1)


def main():
    """Convert question bank to QTI using txttoqti Python API."""
    current_dir = Path(__file__).parent

    # Find question bank file
    question_files = list(current_dir.glob("banco-preguntas-*.txt"))
    if not question_files:
        print("❌ No question bank file found")
        return 1

    input_file = question_files[0]
    output_file = current_dir / "periodo-3-qti.zip"

    # Convert using new txttoqti Python API
    try:
        converter = txttoqti.TxtToQti()
        converter.read_txt(str(input_file)).save_to_qti(str(output_file))
        print(f"✅ QTI package created: {output_file}")
        return 0

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
