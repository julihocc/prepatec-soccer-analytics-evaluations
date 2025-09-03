#!/usr/bin/env python3
"""
CLI principal para el sistema de evaluaciones
Interfaz unificada que usa txttoqti de PyPI con funcionalidades específicas
"""

import argparse
import sys
from pathlib import Path

import subprocess
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
    """Convierte todos los bloques disponibles usando txttoqti-edu CLI."""
    txttoqti_path = find_txttoqti_edu()
    
    if not txttoqti_path:
        print("❌ txttoqti-edu no encontrado")
        print("   Instala: pip install txttoqti>=0.3.0")
        return 1
    
    print("🚀 Conversión masiva de evaluaciones")
    print("=" * 40)
    
    bloques = ['bloque-1', 'bloque-2', 'bloque-3']
    success_count = 0
    
    for bloque in bloques:
        canvas_dir = Path(bloque) / "canvas"
        if canvas_dir.exists():
            print(f"\n📝 Procesando {bloque.upper()}...")
            try:
                result = subprocess.run([
                    txttoqti_path, 
                    "--path", str(canvas_dir),
                    "--verbose"
                ], cwd=Path.cwd())
                
                if result.returncode == 0:
                    print(f"✅ {bloque.upper()} completado")
                    success_count += 1
                else:
                    print(f"❌ Error en {bloque.upper()}")
                    
            except Exception as e:
                print(f"❌ Error procesando {bloque}: {e}")
        else:
            print(f"⚠️  {bloque.upper()}: Directorio canvas no encontrado")
    
    print(f"\n📊 Resumen: {success_count}/{len(bloques)} bloques procesados exitosamente")
    return 0 if success_count > 0 else 1

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
    
    # Para conversión de bloque específico
    if args.path:
        return convert_specific_path(args.path, args.force, args.verbose)
    
    # Si no se especifica ninguna opción, mostrar ayuda
    parser.print_help()
    return 0

def convert_specific_path(path: str, force: bool = False, verbose: bool = False):
    """Convierte archivos en un directorio específico usando txttoqti-edu."""
    txttoqti_path = find_txttoqti_edu()
    
    if not txttoqti_path:
        print("❌ txttoqti-edu no encontrado")
        print("   Instala: pip install txttoqti>=0.3.0")
        return 1
    
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"❌ El directorio {path} no existe")
        return 1
    
    if not path_obj.is_dir():
        print(f"❌ {path} no es un directorio válido")
        return 1
    
    # Construir argumentos para txttoqti-edu
    args = [txttoqti_path, "--path", str(path_obj)]
    if force:
        args.append("--force")
    if verbose:
        args.append("--verbose")
    
    try:
        result = subprocess.run(args, cwd=Path.cwd())
        
        if result.returncode == 0:
            print(f"✅ Conversión completada para {path}")
            return 0
        else:
            print(f"❌ Error en la conversión (código {result.returncode})")
            return 1
            
    except Exception as e:
        print(f"❌ Error ejecutando txttoqti-edu: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())