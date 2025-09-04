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
# Convert all periods to QTI packages (simple script)
./convert-all.sh

# Convert individual periods - three options:
# Option 1: Direct txttoqti
txttoqti -i periodo-1/canvas/banco-preguntas-periodo1.txt -o periodo-1.zip

# Option 2: Per-period Python scripts (simplified)
cd periodo-1/canvas && python3 generar_qti.py
cd periodo-2/canvas && python3 generar_qti.py  
cd periodo-3/canvas && python3 generar_qti.py

# Option 3: From any directory
python3 periodo-1/canvas/generar_qti.py
```

### Testing and Quality Assurance
```bash
# Code formatting
black evaluaciones/ periodo-*/canvas/generar_qti.py

# Linting
ruff check evaluaciones/

# Run tests (if tests directory exists)
pytest
```

## Architecture Overview

### Core Structure
- **`convert-all.sh`**: Simple shell script to convert all question banks
- **`periodo-X/canvas/generar_qti.py`**: Simplified per-period conversion scripts (44 lines each)
- **`txttoqti`**: Direct use of txttoqti v0.4.0 for QTI conversion
- **Question banks**: Use `ANSWER:` format for txttoqti compatibility

### Period Structure Pattern
Each evaluation period (`periodo-1/`, `periodo-2/`, `periodo-3/`) follows this structure:
```
periodo-X/
├── canvas/
│   ├── banco-preguntas-periodoX.txt    # Main question bank (ANSWER: format)
│   ├── preguntas-periodo-X.txt         # Symlink to main file
│   ├── generar_qti.py                 # Simple conversion script (44 lines)
│   └── periodo-X-qti.zip               # Generated QTI package
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
- Symlinks like `preguntas-periodo-X.txt` → `banco-preguntas-periodoX.txt` are supported

## Security Considerations

- Repository contains sensitive academic material (answer keys, complete solutions)
- Never commit to public repositories or share outside authorized academic context
- All CLI tools respect the confidential nature of the content
- `.gitignore` excludes temporary conversion files and local configuration

## Working with the Codebase

### When Modifying Question Banks
1. Edit the `.txt` files in `periodo-X/canvas/` directories
2. Ensure questions use `ANSWER:` format (not `RESPUESTA:`)
3. Test conversion: `txttoqti -i periodo-X/canvas/banco-preguntas-periodoX.txt -o test.zip`
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