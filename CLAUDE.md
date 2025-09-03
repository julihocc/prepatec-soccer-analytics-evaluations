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

### Core CLI Tools
```bash
# Check global status of all evaluation blocks
eval-qti --status

# Convert all blocks to QTI packages
eval-qti --convert-all

# Validate question formats across all blocks
eval-validate --verbose

# Batch processing with parallel execution
eval-batch --force --verbose
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

### Core Module Structure
- **`evaluaciones/`**: Main Python package containing the evaluation system
  - **`cli.py`**: Unified command-line interface (`eval-qti` command)
  - **`batch_converter.py`**: Parallel/sequential batch processing (`eval-batch` command)
  - **`validator.py`**: Question format validation (`eval-validate` command)
  - **`format_converter.py`**: Utility for format conversion between question formats

### Block Structure Pattern
Each evaluation block (`bloque-1/`, `bloque-2/`, `bloque-3/`) follows this structure:
```
bloque-X/
├── canvas/
│   ├── banco-preguntas-bloqueX.txt    # Main question bank
│   ├── preguntas-bloque-X.txt         # Symlink to main file
│   └── generar_qti.py                 # Per-block conversion script
├── caso-practico/                     # Practical case studies
├── datasets/                          # Data files for evaluations
└── rubricas/                          # Evaluation rubrics
```

### Integration with txttoqti

The system integrates with **txttoqti v0.3.0** which provides:
- `txttoqti-edu`: Educational CLI tool that auto-detects question formats
- Native support for the question format used: `Q1:` → `A) B) C) D)` → `RESPUESTA:`
- Automatic Canvas QTI package generation

### Question Format
The system expects questions in this specific format:
```
Q1: What is the result of executing type(42) in Python?
A) <class 'float'>
B) <class 'int'>
C) <class 'str'>
D) <class 'number'>
RESPUESTA: B
```

### CLI Commands Flow
1. **`eval-qti --status`**: Scans all blocks and reports conversion status
2. **`eval-qti --convert-all`**: Calls `txttoqti-edu` on each block's canvas directory
3. **`eval-batch`**: Parallel execution of conversions with progress tracking
4. **`eval-validate`**: Uses txttoqti's validation capabilities + custom validation

## Key Implementation Details

### txttoqti Integration
- All conversion operations delegate to `txttoqti-edu` CLI rather than Python API
- The system finds the `txttoqti-edu` command in `.venv/bin/` or system PATH
- Each block's `generar_qti.py` is a lightweight wrapper around `txttoqti-edu --path`

### Parallel Processing
- `batch_converter.py` uses `concurrent.futures.ThreadPoolExecutor` for parallel conversions
- Default: 3 workers maximum to avoid overwhelming the system
- Falls back to sequential processing for single blocks or when requested

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
2. Run `eval-validate` to check format compliance
3. Use `eval-qti --path bloque-X` to test conversion
4. Verify QTI output before committing

### When Extending Functionality
- Follow the existing CLI pattern: delegate to `txttoqti-edu` rather than reimplementing
- Maintain compatibility with the educational question format
- Use the existing validation and error handling patterns
- Update the corresponding CLI help text and documentation

### Troubleshooting Common Issues
- "txttoqti-edu not found": Ensure txttoqti>=0.3.0 is installed
- "Input file not found": Check that question files follow naming convention
- Format errors: Use `eval-validate --verbose` to identify specific issues
- Conversion failures: Check that working directory is project root when running batch operations