# AI Coding Assistant Instructions

## Project Overview
Educational assessment system for "Ciencia de Datos Aplicada al Fútbol" course at Tecnológico de Monterrey. Converts text-based question banks to Canvas LMS QTI packages using txttoqti library.

**⚠️ CONFIDENTIAL**: Contains sensitive educational material including answer keys and evaluation rubrics. Access restricted to authorized academic personnel.

## Architecture Patterns

### Block Structure Pattern
Each evaluation block follows this structure:
```
bloque-X/
├── canvas/
│   ├── banco-preguntas-bloqueX.txt    # Main question bank
│   ├── preguntas-bloque-X.txt         # Symlink to main file
│   └── generar_qti.py                 # Per-block conversion script
├── caso-practico/                     # Practical case studies
├── datasets/                          # Data files for evaluations
└── solucion-caso-practico/            # Solution files (confidential)
```

### CLI Command Pattern
All CLI tools delegate to `txttoqti-edu` rather than reimplementing conversion logic:
```python
# Pattern: Find txttoqti-edu in virtual environment first
def find_txttoqti_edu() -> Optional[str]:
    current_dir = Path.cwd()
    for _ in range(10):
        venv_bin = current_dir / ".venv" / "bin" / "txttoqti-edu"
        if venv_bin.exists():
            return str(venv_bin)
        current_dir = current_dir.parent
    # Fallback to system PATH
```

### Question Format Standard
Strict format for all question banks:
```
Q1: What is the result of executing type(42) in Python?
A) <class 'float'>
B) <class 'int'>
C) <class 'str'>
D) <class 'number'>
RESPUESTA: B
```

## Development Workflows

### Setup Commands
```bash
# Install in development mode with all dependencies
pip install -e .[dev]

# Install with virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e .[dev]
```

### Core CLI Commands
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

### Code Quality Commands
```bash
# Code formatting
black evaluaciones/ bloque-*/canvas/generar_qti.py

# Linting
ruff check evaluaciones/

# Run tests (if tests directory exists)
pytest
```

## Key Implementation Patterns

### Parallel Processing Pattern
Use `concurrent.futures.ThreadPoolExecutor` for batch operations:
```python
def convert_parallel(bloques: List[str], max_workers: int = 3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(convert_single_block, bloque): bloque for bloque in bloques}
        for future in concurrent.futures.as_completed(futures):
            # Process results as they complete
```

### File Discovery Pattern
Discover question files using glob patterns, filter out temporary files:
```python
txt_files = list(canvas_dir.glob("*.txt"))
# Automatically filters out .checksum, .zip, and other temporary files
```

### Error Handling Pattern
Validate existence before processing:
```python
if not canvas_dir.exists():
    return bloque, False, f"Directorio canvas no encontrado en {bloque}"
```

## Integration Points

### txttoqti Library Integration
- **Version**: txttoqti>=0.3.0 required
- **CLI Tool**: `txttoqti-edu` for educational question format support
- **Pattern**: Delegate all conversion logic to txttoqti, don't reimplement
- **Fallback**: Manual validation if txttoqti parsing fails

### Canvas LMS Integration
- Output: QTI packages compatible with Canvas LMS
- Format: Auto-detected educational question format
- Validation: Use txttoqti's built-in validation capabilities

## Security Considerations

### Confidential Material
- Repository contains complete solutions and answer keys
- Never commit to public repositories
- Access restricted to authorized academic personnel
- `.gitignore` excludes temporary conversion files

### File Handling
- Respect symlinks (e.g., `preguntas-bloque-X.txt` → `banco-preguntas-bloqueX.txt`)
- Handle UTF-8 encoding for Spanish content
- Preserve file modification times for change detection

## Common Patterns to Follow

### When Adding New Blocks
1. Create `bloque-X/` directory structure
2. Add question bank in `canvas/banco-preguntas-bloqueX.txt`
3. Create symlink `preguntas-bloque-X.txt` → main file
4. Add `generar_qti.py` wrapper script
5. Update CLI tools to include new block

### When Modifying Question Banks
1. Edit `.txt` files in `bloque-X/canvas/` directories
2. Run `eval-validate` to check format compliance
3. Use `eval-qti --path bloque-X` to test conversion
4. Verify QTI output before committing

### When Extending CLI Tools
- Follow existing CLI pattern: delegate to `txttoqti-edu`
- Maintain compatibility with educational question format
- Use existing validation and error handling patterns
- Update help text and documentation

## Troubleshooting Patterns

### Common Issues
- **"txttoqti-edu not found"**: Ensure txttoqti>=0.3.0 installed in virtual environment
- **"Input file not found"**: Check question files follow naming convention
- **Format errors**: Use `eval-validate --verbose` for specific issues
- **Conversion failures**: Run from project root directory

### Debug Commands
```bash
# Check txttoqti installation
pip show txttoqti

# Verify virtual environment
which txttoqti-edu

# Test single block conversion
eval-qti --path bloque-1 --verbose
```
