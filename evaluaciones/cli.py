#!/usr/bin/env python3
"""
CLI principal para el sistema de evaluaciones
Interfaz unificada que envuelve txttoqti-edu con funcionalidades específicas
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

def find_txttoqti_edu() -> Optional[str]:
    """Encuentra el comando txttoqti-edu en el sistema."""
    # Buscar en entorno virtual primero
    current_dir = Path.cwd()
    for _ in range(10):  # Buscar hasta 10 niveles arriba
        venv_bin = current_dir / ".venv" / "bin" / "txttoqti-edu"
        if venv_bin.exists():
            return str(venv_bin)
        current_dir = current_dir.parent
        if current_dir == current_dir.parent:  # Raíz del sistema
            break
    
    # Buscar en PATH del sistema
    try:
        result = subprocess.run(['which', 'txttoqti-edu'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def show_global_status():
    """Muestra estado global de todos los bloques."""
    print("🎯 Sistema de Evaluaciones - Estado Global")
    print("=" * 50)
    
    bloques = ['bloque-1', 'bloque-2', 'bloque-3']
    for bloque in bloques:
        bloque_path = Path(bloque)
        if bloque_path.exists():
            canvas_dir = bloque_path / "canvas"
            if canvas_dir.exists():
                txt_files = list(canvas_dir.glob("*.txt"))
                zip_files = list(canvas_dir.glob("*.zip"))
                print(f"📁 {bloque.upper()}")
                print(f"   Archivos TXT: {len(txt_files)}")
                print(f"   Archivos ZIP: {len(zip_files)}")
                print(f"   Estado: {'✅ Actualizado' if zip_files else '⚠️  Pendiente'}")
        print()

def convert_all_blocks():
    """Convierte todos los bloques disponibles."""
    txttoqti_path = find_txttoqti_edu()
    
    if not txttoqti_path:
        print("❌ txttoqti-edu no encontrado")
        print("   Instala: pip install git+https://github.com/julihocc/txttoqti.git@v0.3.0")
        return 1
    
    print("🚀 Conversión masiva de evaluaciones")
    print("=" * 40)
    
    bloques = ['bloque-1', 'bloque-2', 'bloque-3']
    for bloque in bloques:
        canvas_dir = Path(bloque) / "canvas"
        if canvas_dir.exists():
            print(f"\n📝 Procesando {bloque.upper()}...")
            try:
                result = subprocess.run([
                    txttoqti_path, 
                    "--path", str(canvas_dir),
                    "--verbose"
                ], cwd=canvas_dir)
                
                if result.returncode == 0:
                    print(f"✅ {bloque.upper()} completado")
                else:
                    print(f"❌ Error en {bloque.upper()}")
                    
            except Exception as e:
                print(f"❌ Error procesando {bloque}: {e}")
    
    return 0

def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema de Evaluaciones - Ciencia de Datos Aplicada al Fútbol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    eval-qti --status          # Ver estado global
    eval-qti --convert-all     # Convertir todos los bloques
    eval-qti --path bloque-1   # Convertir bloque específico
    eval-qti --verbose         # Salida detallada
        """
    )
    
    parser.add_argument("--status", action="store_true",
                       help="Mostrar estado global sin conversión")
    parser.add_argument("--convert-all", action="store_true",
                       help="Convertir todos los bloques disponibles")
    parser.add_argument("--path", type=str,
                       help="Convertir bloque específico")
    parser.add_argument("--verbose", action="store_true",
                       help="Salida detallada")
    parser.add_argument("--force", action="store_true",
                       help="Forzar regeneración")
    parser.add_argument("--interactive", action="store_true",
                       help="Modo interactivo")
    
    args = parser.parse_args()
    
    # Manejo de opciones específicas
    if args.status:
        show_global_status()
        return 0
    
    if args.convert_all:
        return convert_all_blocks()
    
    # Para otras opciones, delegar a txttoqti-edu
    txttoqti_path = find_txttoqti_edu()
    
    if not txttoqti_path:
        print("❌ txttoqti-edu no encontrado")
        print("   Instala: pip install git+https://github.com/julihocc/txttoqti.git@v0.3.0")
        return 1
    
    # Construir argumentos para txttoqti-edu
    txttoqti_args = [txttoqti_path]
    
    if args.path:
        txttoqti_args.extend(["--path", args.path])
    if args.verbose:
        txttoqti_args.append("--verbose")
    if args.force:
        txttoqti_args.append("--force")
    if args.interactive:
        txttoqti_args.append("--interactive")
    
    try:
        result = subprocess.run(txttoqti_args)
        return result.returncode
    except Exception as e:
        print(f"❌ Error ejecutando txttoqti-edu: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())