#!/usr/bin/env python3
"""
Validador de evaluaciones
Verifica formato y contenido de archivos de evaluación usando txttoqti
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

try:
    from txttoqti import QuestionValidator, QuestionParser
    from txttoqti.exceptions import TxtToQtiError, ValidationError, ParseError
except ImportError as e:
    print(f"❌ Error: txttoqti no está instalado: {e}")
    print("   Instala con: pip install txttoqti>=0.1.2")
    sys.exit(1)

def validate_question_format(content: str, file_path: Path) -> List[str]:
    """Valida el formato de preguntas usando txttoqti."""
    errors = []
    
    try:
        # Usar el parser de txttoqti para validar
        parser = QuestionParser()
        validator = QuestionValidator()
        
        # Intentar parsear las preguntas
        questions = parser.parse(content)
        
        if not questions:
            errors.append("No se encontraron preguntas válidas en el archivo")
            return errors
        
        # Validar cada pregunta parseada
        for i, question in enumerate(questions, 1):
            try:
                # El parser ya valida la estructura básica
                # Usar el validador para verificaciones adicionales
                is_valid = validator.validate(question)
                if not is_valid:
                    errors.append(f"Pregunta {i}: Formato inválido según validador txttoqti")
            except ValidationError as e:
                errors.append(f"Pregunta {i}: {str(e)}")
            except Exception as e:
                errors.append(f"Pregunta {i}: Error de validación: {str(e)}")
        
        # Información adicional si se parsearon preguntas correctamente
        if not errors:
            return []  # Todo válido
            
    except ParseError as e:
        errors.append(f"Error de parseo: {str(e)}")
    except Exception as e:
        # Fallback a validación manual si txttoqti falla
        return validate_question_format_manual(content, file_path)
    
    return errors

def validate_question_format_manual(content: str, file_path: Path) -> List[str]:
    """Validación manual como fallback."""
    errors = []
    lines = content.split('\n')
    
    question_pattern = r'^Q\d+:'
    answer_pattern = r'^[A-Z]\)'
    
    current_question = None
    has_answers = False
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        # Detectar nueva pregunta
        if re.match(question_pattern, line):
            # Validar pregunta anterior
            if current_question is not None and not has_answers:
                errors.append(f"Línea {current_question}: Pregunta sin respuestas válidas")
            
            current_question = line_num
            has_answers = False
            continue
        
        # Detectar respuesta
        if re.match(answer_pattern, line):
            if current_question is None:
                errors.append(f"Línea {line_num}: Respuesta sin pregunta")
            else:
                has_answers = True
            continue
        
        # Líneas que no siguen el formato
        if current_question is not None and line and not has_answers:
            # Permitir líneas de continuación de pregunta
            continue
    
    # Validar última pregunta
    if current_question is not None and not has_answers:
        errors.append(f"Línea {current_question}: Pregunta sin respuestas válidas")
    
    return errors

def validate_file_structure(bloque_path: Path) -> Dict[str, List[str]]:
    """Valida la estructura de archivos de un bloque."""
    errors = {}
    
    # Verificar directorios requeridos
    required_dirs = ['canvas', 'caso-practico', 'rubricas']
    for dir_name in required_dirs:
        dir_path = bloque_path / dir_name
        if not dir_path.exists():
            errors[f"estructura_{dir_name}"] = [f"Directorio {dir_name} no existe"]
        elif not dir_path.is_dir():
            errors[f"estructura_{dir_name}"] = [f"{dir_name} no es un directorio"]
    
    # Validar archivos Canvas
    canvas_dir = bloque_path / "canvas"
    if canvas_dir.exists():
        txt_files = list(canvas_dir.glob("*.txt"))
        if not txt_files:
            errors["canvas_txt"] = ["No se encontraron archivos .txt en canvas/"]
        else:
            for txt_file in txt_files:
                try:
                    content = txt_file.read_text(encoding='utf-8')
                    file_errors = validate_question_format(content, txt_file)
                    if file_errors:
                        errors[f"canvas_{txt_file.name}"] = file_errors
                except Exception as e:
                    errors[f"canvas_{txt_file.name}"] = [f"Error leyendo archivo: {e}"]
    
    return errors

def validate_evaluaciones() -> int:
    """Valida todas las evaluaciones disponibles."""
    print("🔍 Validador de Evaluaciones")
    print("=" * 30)
    
    base_path = Path.cwd()
    bloques = ['bloque-1', 'bloque-2', 'bloque-3']
    
    total_errors = 0
    
    for bloque in bloques:
        bloque_path = base_path / bloque
        if not bloque_path.exists():
            print(f"⚠️  {bloque.upper()}: Directorio no encontrado")
            continue
        
        print(f"\n📁 Validando {bloque.upper()}...")
        errors = validate_file_structure(bloque_path)
        
        if errors:
            total_errors += sum(len(err_list) for err_list in errors.values())
            for category, error_list in errors.items():
                print(f"❌ {category}:")
                for error in error_list:
                    print(f"   - {error}")
        else:
            print(f"✅ {bloque.upper()}: Sin errores detectados")
    
    print(f"\n📊 Resumen: {total_errors} errores encontrados")
    return 0 if total_errors == 0 else 1

def main():
    """Función principal del validador."""
    parser = argparse.ArgumentParser(
        description="Validador de evaluaciones para Ciencia de Datos Aplicada al Fútbol"
    )
    
    parser.add_argument("--bloque", type=str,
                       help="Validar bloque específico (bloque-1, bloque-2, bloque-3)")
    parser.add_argument("--verbose", action="store_true",
                       help="Salida detallada")
    
    args = parser.parse_args()
    
    if args.bloque:
        bloque_path = Path(args.bloque)
        if not bloque_path.exists():
            print(f"❌ Bloque {args.bloque} no encontrado")
            return 1
        
        print(f"🔍 Validando {args.bloque.upper()}...")
        errors = validate_file_structure(bloque_path)
        
        if errors:
            for category, error_list in errors.items():
                print(f"❌ {category}:")
                for error in error_list:
                    print(f"   - {error}")
            return 1
        else:
            print(f"✅ {args.bloque.upper()}: Sin errores detectados")
            return 0
    else:
        return validate_evaluaciones()

if __name__ == "__main__":
    sys.exit(main())