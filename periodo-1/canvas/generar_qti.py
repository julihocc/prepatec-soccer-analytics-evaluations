#!/usr/bin/env python3
"""Simple QTI generator for período-1."""

import subprocess
import sys
from pathlib import Path

def main():
    """Convert question bank to QTI using txttoqti."""
    current_dir = Path(__file__).parent
    
    # Find question bank file
    question_files = list(current_dir.glob("banco-preguntas-*.txt"))
    if not question_files:
        print("❌ No question bank file found")
        return 1
    
    input_file = question_files[0]
    output_file = current_dir / "periodo-1-qti.zip"
    
    # Run txttoqti conversion
    try:
        result = subprocess.run([
            "txttoqti", 
            "-i", str(input_file),
            "-o", str(output_file)
        ], check=False, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ QTI package created: {output_file}")
            return 0
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return 1
            
    except FileNotFoundError:
        print("❌ txttoqti not found. Install with: pip install txttoqti>=0.4.0")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())