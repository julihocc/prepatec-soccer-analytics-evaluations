#!/usr/bin/env python3
"""
Conversor de formatos para compatibilidad con txttoqti PyPI
Convierte el formato usado en las evaluaciones al formato esperado por txttoqti
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional


def convert_question_format(content: str) -> str:
    """
    Convierte del formato de evaluaciones al formato txttoqti.
    
    Formato de entrada:
        Q1: Pregunta aquí?
        A) Opción 1
        B) Opción 2
        C) Opción 3
        D) Opción 4
        RESPUESTA: B
    
    Formato de salida:
        1. Pregunta aquí?
        a) Opción 1
        b) Opción 2
        c) Opción 3
        d) Opción 4
        *b
    """
    lines = content.strip().split('\n')
    converted_lines = []
    current_question = {}
    question_counter = 0
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Detectar nueva pregunta (Q1:, Q2:, etc.)
        question_match = re.match(r'^Q(\d+):\s*(.+)', line)
        if question_match:
            # Finalizar pregunta anterior si existe
            if current_question:
                _add_converted_question(converted_lines, current_question)
                current_question = {}
            
            question_counter += 1
            question_text = question_match.group(2)
            current_question = {
                'number': question_counter,
                'text': question_text,
                'choices': [],
                'correct_answer': None
            }
            i += 1
            continue
        
        # Detectar opciones de respuesta (A), B), C), D))
        choice_match = re.match(r'^([A-Z])\)\s*(.+)', line)
        if choice_match and current_question:
            choice_letter = choice_match.group(1).lower()
            choice_text = choice_match.group(2)
            current_question['choices'].append({
                'letter': choice_letter,
                'text': choice_text
            })
            i += 1
            continue
        
        # Detectar respuesta correcta
        answer_match = re.match(r'^RESPUESTA:\s*([A-Z])', line)
        if answer_match and current_question:
            correct_letter = answer_match.group(1).lower()
            current_question['correct_answer'] = correct_letter
            i += 1
            continue
        
        # Si estamos en una pregunta, podría ser continuación del texto
        if current_question and 'text' in current_question:
            current_question['text'] += ' ' + line
        
        i += 1
    
    # Finalizar última pregunta
    if current_question:
        _add_converted_question(converted_lines, current_question)
    
    return '\n'.join(converted_lines)


def _add_converted_question(converted_lines: List[str], question: dict):
    """Añade una pregunta convertida a la lista de líneas."""
    if not question.get('text') or not question.get('choices'):
        return
    
    # Add blank line between questions (except for first)
    if converted_lines:
        converted_lines.append('')
    
    question_text = f"{question['number']}. {question['text']}"
    converted_lines.append(question_text)
    
    for choice in question['choices']:
        choice_line = f"{choice['letter']}) {choice['text']}"
        converted_lines.append(choice_line)
    
    # Añadir respuesta correcta
    if question.get('correct_answer'):
        correct_line = f"*{question['correct_answer']}"
        converted_lines.append(correct_line)


def convert_file(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convierte un archivo del formato de evaluaciones al formato txttoqti.
    
    Args:
        input_path: Ruta del archivo de entrada
        output_path: Ruta del archivo de salida (opcional)
        
    Returns:
        Path del archivo convertido
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {input_path}")
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_txttoqti_format.txt"
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        converted_content = convert_question_format(original_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return output_path
        
    except Exception as e:
        raise RuntimeError(f"Error convirtiendo archivo {input_path}: {e}")


def main():
    """Función principal para pruebas."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Conversor de formatos de preguntas")
    parser.add_argument("input_file", help="Archivo de entrada")
    parser.add_argument("-o", "--output", help="Archivo de salida (opcional)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output) if args.output else None
    
    try:
        result_path = convert_file(input_path, output_path)
        print(f"✅ Archivo convertido: {result_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())