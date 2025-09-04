# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational assessment system for "Ciencia de Datos Aplicada al Fútbol" course at Tecnológico de Monterrey. It converts text-based question banks to Canvas LMS QTI packages using the txttoqti library.

**⚠️ CONFIDENTIAL REPOSITORY**: Contains sensitive educational material including answer keys, test cases, and evaluation rubrics. Access restricted to authorized academic personnel.

## Development Commands

### Setup and Installation
```bash
# Install in development mode with all dependencies
pip install -e .[dev]

# Install with virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e .[dev]
```

### Core Conversion Tools
```bash
# Convert all blocks to QTI packages (simple script)
./convert-all.sh

# Convert individual blocks - three options:
# Option 1: Direct txttoqti
txttoqti -i bloque-1/canvas/banco-preguntas-bloque1.txt -o bloque-1.zip

# Option 2: Per-block Python scripts (simplified)
cd bloque-1/canvas && python3 generar_qti.py
cd bloque-2/canvas && python3 generar_qti.py  
cd bloque-3/canvas && python3 generar_qti.py

# Option 3: From any directory
python3 bloque-1/canvas/generar_qti.py
```

### Testing and Quality Assurance
```bash
# Code formatting
black evaluaciones/ bloque-*/canvas/generar_qti.py

# Linting
ruff check evaluaciones/

# Run tests (if tests directory exists)
pytest
```

## Architecture Overview

### Core Structure
- **`convert-all.sh`**: Simple shell script to convert all question banks
- **`bloque-X/canvas/generar_qti.py`**: Simplified per-block conversion scripts (44 lines each)
- **`txttoqti`**: Direct use of txttoqti v0.4.0 for QTI conversion
- **Question banks**: Use `ANSWER:` format for txttoqti compatibility

### Block Structure Pattern
Each evaluation block (`bloque-1/`, `bloque-2/`, `bloque-3/`) follows this structure:
```
bloque-X/
├── canvas/
│   ├── banco-preguntas-bloqueX.txt    # Main question bank (ANSWER: format)
│   ├── preguntas-bloque-X.txt         # Symlink to main file
│   ├── generar_qti.py                 # Simple conversion script (44 lines)
│   └── bloque-X-qti.zip               # Generated QTI package
├── caso-practico/                     # Practical case studies
├── datasets/                          # Data files for evaluations
└── rubricas/                          # Evaluation rubrics
```

### Integration with txttoqti

The system uses **txttoqti v0.4.0** directly:
- Direct CLI usage: `txttoqti -i input.txt -o output.zip`
- Native support for the question format: `Q1:` → `A) B) C) D)` → `ANSWER:`
- Automatic Canvas QTI package generation

### Question Format
The system expects questions in this specific format:
```
Q1: What is the result of executing type(42) in Python?
A) <class 'float'>
B) <class 'int'>
C) <class 'str'>
D) <class 'number'>
ANSWER: B
```

### Conversion Workflow
1. **`./convert-all.sh`**: Convert all question banks to QTI format
2. **`txttoqti -i input.txt -o output.zip`**: Direct conversion of individual files
3. **Built-in validation**: txttoqti v0.4.0 validates format automatically

## Key Implementation Details

### Simplified Integration
- Direct use of `txttoqti` CLI for all conversions
- Simple shell script (`convert-all.sh`) handles batch processing
- No complex wrappers or custom Python modules needed

### File Discovery Pattern
- Question files are discovered via glob patterns: `*.txt` in canvas directories
- Log files and temporary files are automatically filtered out
- Symlinks like `preguntas-bloque-X.txt` → `banco-preguntas-bloqueX.txt` are supported

## Security Considerations

- Repository contains sensitive academic material (answer keys, complete solutions)
- Never commit to public repositories or share outside authorized academic context
- All CLI tools respect the confidential nature of the content
- `.gitignore` excludes temporary conversion files and local configuration

## Working with the Codebase

### When Modifying Question Banks
1. Edit the `.txt` files in `bloque-X/canvas/` directories
2. Ensure questions use `ANSWER:` format (not `RESPUESTA:`)
3. Test conversion: `txttoqti -i bloque-X/canvas/banco-preguntas-bloqueX.txt -o test.zip`
4. Verify QTI output before committing

### When Extending Functionality
- Use txttoqti directly rather than creating wrappers
- Maintain compatibility with the `ANSWER:` format
- Use txttoqti's built-in validation
- Update the conversion script if needed

### Troubleshooting Common Issues
- "txttoqti not found": Ensure txttoqti>=0.4.0 is installed (`pip install txttoqti>=0.4.0`)
- "Input file not found": Check file paths in conversion commands
- "Multiple choice question has no correct answer": Ensure `ANSWER:` field exactly matches one of the answer options (A, B, C, D)
- Conversion failures: Use `./convert-all.sh` from project root, or check individual file paths