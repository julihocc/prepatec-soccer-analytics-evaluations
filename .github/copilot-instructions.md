# AI Coding Assistant Instructions

## Project Overview
Educational assessment system for "Ciencia de Datos Aplicada al Fútbol" course at Tecnológico de Monterrey. Converts text-based question banks to Canvas LMS QTI packages using txttoqti v0.4.0 directly.

**⚠️ CONFIDENTIAL**: Contains sensitive educational material including answer keys and evaluation rubrics. Access restricted to authorized academic personnel.

## Architecture Patterns

### Block Structure Pattern
Each evaluation block follows this structure:
```
bloque-X/
├── canvas/
│   ├── banco-preguntas-bloqueX.txt    # Main question bank (ANSWER: format)
│   ├── preguntas-bloque-X.txt         # Symlink to main file
│   ├── generar_qti.py                 # Simple conversion script (44 lines)
│   └── bloque-X-qti.zip               # Generated QTI package
├── caso-practico/                     # Practical case studies
├── datasets/                          # Data files for evaluations
└── solucion-caso-practico/            # Solution files (confidential)
```

### Conversion Pattern
Simple, direct usage of txttoqti v0.4.0:
```bash
# Batch conversion (recommended)
./convert-all.sh

# Individual conversion
cd bloque-X/canvas && python3 generar_qti.py

# Direct txttoqti usage
txttoqti -i input.txt -o output.zip
```

### Question Format Standard
Strict format for all question banks:
```
Q1: What is the result of executing type(42) in Python?
A) <class 'float'>
B) <class 'int'>
C) <class 'str'>
D) <class 'number'>
ANSWER: B
```

## Development Workflows

### Setup Commands
```bash
# Install txttoqti dependency
pip install txttoqti>=0.4.0

# Install with virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install txttoqti>=0.4.0
```

### Core Conversion Commands
```bash
# Convert all blocks to QTI
./convert-all.sh

# Convert individual blocks
cd bloque-1/canvas && python3 generar_qti.py
cd bloque-2/canvas && python3 generar_qti.py
cd bloque-3/canvas && python3 generar_qti.py

# Direct txttoqti usage
txttoqti -i bloque-1/canvas/banco-preguntas-bloque1.txt -o bloque-1.zip
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
2. Run `txttoqti validation` to check format compliance
3. Use `python3 bloque-X/canvas/generar_qti.py` to test conversion
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
- **Format errors**: Use `txttoqti validation --verbose` for specific issues
- **Conversion failures**: Run from project root directory

### Debug Commands
```bash
# Check txttoqti installation
pip show txttoqti

# Verify virtual environment
which txttoqti-edu

# Test single block conversion
python3 bloque-1/canvas/generar_qti.py
```
