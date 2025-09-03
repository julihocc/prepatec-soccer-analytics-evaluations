#!/usr/bin/env python3
"""
Conversor en lotes para múltiples evaluaciones
Procesa todos los bloques o bloques específicos de manera eficiente
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional
import concurrent.futures
import time

def find_txttoqti_edu() -> Optional[str]:
    """Encuentra el comando txttoqti-edu."""
    current_dir = Path.cwd()
    for _ in range(10):
        venv_bin = current_dir / ".venv" / "bin" / "txttoqti-edu"
        if venv_bin.exists():
            return str(venv_bin)
        current_dir = current_dir.parent
        if current_dir == current_dir.parent:
            break
    
    try:
        result = subprocess.run(['which', 'txttoqti-edu'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def convert_single_block(bloque: str, force: bool = False, verbose: bool = False) -> tuple[str, bool, str]:
    """Convierte un bloque individual."""
    txttoqti_path = find_txttoqti_edu()
    
    if not txttoqti_path:
        return bloque, False, "txttoqti-edu no encontrado"
    
    canvas_dir = Path(bloque) / "canvas"
    if not canvas_dir.exists():
        return bloque, False, f"Directorio canvas no encontrado en {bloque}"
    
    # Construir argumentos
    args = [txttoqti_path, "--path", str(canvas_dir)]
    if force:
        args.append("--force")
    if verbose:
        args.append("--verbose")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            args,
            cwd=canvas_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo por bloque
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            message = f"Completado en {duration:.1f}s"
            if verbose and result.stdout:
                message += f"\n{result.stdout}"
            return bloque, True, message
        else:
            error_msg = f"Error (código {result.returncode})"
            if result.stderr:
                error_msg += f": {result.stderr}"
            return bloque, False, error_msg
            
    except subprocess.TimeoutExpired:
        return bloque, False, "Timeout (>5 minutos)"
    except Exception as e:
        return bloque, False, f"Excepción: {e}"

def convert_parallel(bloques: List[str], force: bool = False, verbose: bool = False, max_workers: int = 3):
    """Convierte múltiples bloques en paralelo."""
    print(f"🚀 Conversión en paralelo de {len(bloques)} bloques")
    print(f"   Trabajadores: {max_workers}")
    print("=" * 50)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Enviar tareas
        futures = {
            executor.submit(convert_single_block, bloque, force, verbose): bloque
            for bloque in bloques
        }
        
        # Procesar resultados conforme se completan
        results = []
        for future in concurrent.futures.as_completed(futures):
            bloque_name = futures[future]
            try:
                bloque, success, message = future.result()
                results.append((bloque, success, message))
                
                if success:
                    print(f"✅ {bloque.upper()}: {message}")
                else:
                    print(f"❌ {bloque.upper()}: {message}")
                    
            except Exception as e:
                print(f"❌ {bloque_name.upper()}: Error inesperado: {e}")
                results.append((bloque_name, False, f"Error inesperado: {e}"))
    
    # Resumen final
    successful = sum(1 for _, success, _ in results if success)
    print(f"\n📊 Resumen: {successful}/{len(bloques)} bloques convertidos exitosamente")
    
    return successful == len(bloques)

def convert_sequential(bloques: List[str], force: bool = False, verbose: bool = False):
    """Convierte bloques de manera secuencial."""
    print(f"🔄 Conversión secuencial de {len(bloques)} bloques")
    print("=" * 40)
    
    successful = 0
    
    for i, bloque in enumerate(bloques, 1):
        print(f"\n📝 [{i}/{len(bloques)}] Procesando {bloque.upper()}...")
        
        bloque_name, success, message = convert_single_block(bloque, force, verbose)
        
        if success:
            print(f"✅ {message}")
            successful += 1
        else:
            print(f"❌ {message}")
    
    print(f"\n📊 Resumen: {successful}/{len(bloques)} bloques convertidos exitosamente")
    return successful == len(bloques)

def convert_all_blocks(force: bool = False, verbose: bool = False, parallel: bool = True):
    """Convierte todos los bloques disponibles."""
    base_path = Path.cwd()
    bloques_disponibles = []
    
    for bloque in ['bloque-1', 'bloque-2', 'bloque-3']:
        canvas_dir = base_path / bloque / "canvas"
        if canvas_dir.exists():
            bloques_disponibles.append(bloque)
    
    if not bloques_disponibles:
        print("❌ No se encontraron bloques con directorio canvas")
        return False
    
    print(f"🎯 Bloques detectados: {', '.join(b.upper() for b in bloques_disponibles)}")
    
    if parallel and len(bloques_disponibles) > 1:
        return convert_parallel(bloques_disponibles, force, verbose)
    else:
        return convert_sequential(bloques_disponibles, force, verbose)

def main():
    """Función principal del conversor en lotes."""
    parser = argparse.ArgumentParser(
        description="Conversor en lotes para evaluaciones",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    eval-batch                          # Convertir todos los bloques (paralelo)
    eval-batch --sequential            # Convertir todos los bloques (secuencial)
    eval-batch --bloques bloque-1 bloque-3  # Convertir bloques específicos
    eval-batch --force --verbose       # Forzar regeneración con salida detallada
        """
    )
    
    parser.add_argument("--bloques", nargs="+",
                       help="Bloques específicos a convertir")
    parser.add_argument("--force", action="store_true",
                       help="Forzar regeneración incluso si no hay cambios")
    parser.add_argument("--verbose", action="store_true",
                       help="Salida detallada")
    parser.add_argument("--sequential", action="store_true",
                       help="Procesamiento secuencial en lugar de paralelo")
    parser.add_argument("--max-workers", type=int, default=3,
                       help="Número máximo de trabajadores paralelos (defecto: 3)")
    
    args = parser.parse_args()
    
    if args.bloques:
        # Validar bloques especificados
        bloques_validos = []
        for bloque in args.bloques:
            canvas_dir = Path(bloque) / "canvas"
            if canvas_dir.exists():
                bloques_validos.append(bloque)
            else:
                print(f"⚠️  Ignorando {bloque}: directorio canvas no encontrado")
        
        if not bloques_validos:
            print("❌ Ningún bloque válido especificado")
            return 1
        
        if args.sequential or len(bloques_validos) == 1:
            success = convert_sequential(bloques_validos, args.force, args.verbose)
        else:
            success = convert_parallel(bloques_validos, args.force, args.verbose, args.max_workers)
    else:
        # Convertir todos los bloques
        success = convert_all_blocks(args.force, args.verbose, not args.sequential)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())