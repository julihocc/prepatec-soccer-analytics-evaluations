#!/usr/bin/env python3
"""
🚀 QTI GENERATOR - txttoqti PyPI Integration
Direct integration with txttoqti from PyPI for robust QTI conversion.

This script converts text-based question banks to Canvas-compatible QTI packages
using the official txttoqti library from PyPI.

Features:
- Direct Python API integration (no subprocess calls)
- Uses txttoqti v0.1.2+ from PyPI
- Automatic file discovery and conversion
- Smart change detection to avoid unnecessary regeneration
- Enhanced error handling and validation

Usage:
    python generar_qti.py [--status] [--force] [--help]
    
Arguments:
    --status        Show current status without conversion
    --force         Force regeneration even if no changes detected
    --help          Show help message
"""

import sys
from pathlib import Path
import argparse

import subprocess
from typing import Optional

def find_txttoqti_edu() -> Optional[str]:
    """Find txttoqti-edu command in virtual environment or system PATH."""
    # Try virtual environment first
    script_dir = Path(__file__).parent
    
    # Walk up to find repository root with .venv
    current_dir = script_dir
    for _ in range(10):  # Search up to 10 levels up
        venv_bin = current_dir / ".venv" / "bin" / "txttoqti-edu"
        if venv_bin.exists():
            return str(venv_bin)
        current_dir = current_dir.parent
        if current_dir == current_dir.parent:  # Reached filesystem root
            break
    
    # Try system PATH
    try:
        result = subprocess.run(['which', 'txttoqti-edu'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None


def show_status():
    """Show current status using txttoqti-edu."""
    txttoqti_edu_path = find_txttoqti_edu()
    
    if not txttoqti_edu_path:
        print("❌ Error: txttoqti-edu no encontrado")
        print("   Instala txttoqti v0.3.0+: pip install txttoqti>=0.3.0")
        return
    
    current_dir = Path(__file__).parent
    
    try:
        result = subprocess.run([
            txttoqti_edu_path, 
            "--status", 
            "--path", str(current_dir)
        ])
        
        if result.returncode != 0:
            print(f"❌ Error mostrando estado")
            
    except Exception as e:
        print(f"❌ Error ejecutando txttoqti-edu: {e}")


def convert_files(force=False):
    """Convert files using txttoqti-edu."""
    txttoqti_edu_path = find_txttoqti_edu()
    
    if not txttoqti_edu_path:
        print("❌ Error: txttoqti-edu no encontrado")
        print("   Instala txttoqti v0.3.0+: pip install txttoqti>=0.3.0")
        return False
    
    current_dir = Path(__file__).parent
    
    # Construir argumentos
    args = [txttoqti_edu_path, "--path", str(current_dir)]
    if force:
        args.append("--force")
    
    try:
        result = subprocess.run(args)
        
        if result.returncode == 0:
            print("✅ Conversión completada")
            return True
        else:
            print(f"❌ Error en conversión (código {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando txttoqti-edu: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Generador QTI para evaluaciones de fútbol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    python generar_qti.py              # Convertir archivos nuevos o modificados
    python generar_qti.py --status     # Ver estado actual
    python generar_qti.py --force      # Forzar regeneración de todos los archivos
        """
    )
    
    parser.add_argument("--status", action="store_true",
                       help="Mostrar estado actual sin conversión")
    parser.add_argument("--force", action="store_true",
                       help="Forzar regeneración de todos los archivos")
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
        return 0
    
    success = convert_files(force=args.force)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())