#!/usr/bin/env python3
"""Convert all question banks using txttoqti v0.5.0 Python API."""

import sys
from pathlib import Path

try:
    import txttoqti
except ImportError:
    print("❌ txttoqti not found. Install with: pip install txttoqti>=0.5.0")
    sys.exit(1)


def main():
    """Convert all question banks to QTI format using Python API."""
    print("🎯 Converting question banks to QTI format...")
    print("==============================================")

    project_root = Path(__file__).parent
    success_count = 0
    total_periods = 0

    # Convert each period
    for periodo_dir in project_root.glob("periodo-*"):
        if not periodo_dir.is_dir():
            continue

        canvas_dir = periodo_dir / "canvas"
        if not canvas_dir.exists():
            print(f"   ⚠️  Directory {canvas_dir} not found")
            continue

        # Find question bank file
        question_files = list(canvas_dir.glob("banco-preguntas-*.txt"))
        if not question_files:
            print(f"   ⚠️  No question file found in {canvas_dir}")
            continue

        input_file = question_files[0]
        output_file = canvas_dir / f"{periodo_dir.name}-qti.zip"

        print(f"📝 Converting {periodo_dir.name}...")
        total_periods += 1

        try:
            converter = txttoqti.TxtToQti()
            converter.read_txt(str(input_file)).save_to_qti(str(output_file))
            print(f"   ✅ {output_file} created successfully")
            success_count += 1

        except Exception as e:
            print(f"   ❌ Failed to convert {periodo_dir.name}: {e}")

    print()
    if success_count == total_periods:
        print("🎉 All conversions completed successfully!")
        print("📁 QTI files are in each período's canvas directory")
        return 0
    else:
        print(f"⚠️  Completed {success_count}/{total_periods} conversions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
