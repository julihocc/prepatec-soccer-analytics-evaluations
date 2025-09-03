"""
Ciencia de Datos Aplicada al Fútbol - Sistema de Evaluaciones
Tecnológico de Monterrey

Sistema evaluativo independiente con herramientas para:
- Conversión automática de preguntas de texto a QTI Canvas
- Validación de formatos y contenido
- Procesamiento en lotes de múltiples bloques
- Integración con txttoqti v0.3.0+ desde PyPI

Uso:
    eval-qti --status          # Ver estado global
    eval-qti --convert-all     # Conversión masiva
    eval-validate             # Validar formatos
"""

__version__ = "1.0.0"
__author__ = "Julio César Hernández Castillo"
__email__ = "julio.hernandez@tec.mx"

from .cli import main as cli_main
from .validator import validate_evaluaciones
from .batch_converter import convert_all_blocks

__all__ = [
    "__version__",
    "cli_main", 
    "validate_evaluaciones",
    "convert_all_blocks"
]