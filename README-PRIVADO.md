# Ciencia de Datos Aplicada al Fútbol - Sistema de Evaluaciones

**🔒 REPOSITORIO PRIVADO - USO ACADÉMICO EXCLUSIVO**  
**Tecnológico de Monterrey - Preparatoria**

---

## ⚠️ Confidencialidad

Este repositorio contiene material evaluativo sensible:
- Bancos de preguntas con respuestas correctas
- Casos prácticos con soluciones completas
- Rúbricas de evaluación detalladas
- Datasets específicos para evaluaciones

**ACCESO RESTRINGIDO** a personal académico autorizado del Tecnológico de Monterrey.

---

## 🏗️ Configuración Inicial

### Instalación Rápida

```bash
# 1. Clonar repositorio privado
git clone <url-privado> ciencia-datos-futbol-evaluaciones
cd ciencia-datos-futbol-evaluaciones

# 2. Instalar dependencias
pip install -e .

# 3. Verificar instalación
eval-qti --status
```

### Instalación con Entorno Virtual (Recomendado)

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 2. Instalar en modo desarrollo
pip install -e .[dev]

# 3. Verificar herramientas disponibles
eval-qti --help
eval-validate --help  
eval-batch --help
```

---

## 🎯 Herramientas Disponibles

### 1. CLI Principal (`eval-qti`)

```bash
# Estado global de todos los bloques
eval-qti --status

# Conversión masiva de todos los bloques
eval-qti --convert-all

# Convertir bloque específico
eval-qti --path bloque-1

# Forzar regeneración con salida detallada
eval-qti --force --verbose
```

### 2. Validador (`eval-validate`)

```bash
# Validar todas las evaluaciones
eval-validate

# Validar bloque específico
eval-validate --bloque bloque-2

# Validación detallada
eval-validate --verbose
```

### 3. Conversor en Lotes (`eval-batch`)

```bash
# Conversión paralela de todos los bloques (defecto)
eval-batch

# Conversión secuencial
eval-batch --sequential

# Bloques específicos con fuerza
eval-batch --bloques bloque-1 bloque-3 --force

# Control de paralelismo
eval-batch --max-workers 2 --verbose
```

---

## 📁 Estructura del Repositorio

```
ciencia-datos-futbol-evaluaciones/
├── 📄 README-PRIVADO.md          # Este archivo
├── 📄 SECURITY.md                # Políticas de seguridad
├── 📄 pyproject.toml             # Configuración del proyecto
├── 📄 requirements.txt           # Dependencias pip
├── 📦 evaluaciones/              # Paquete Python principal
│   ├── __init__.py               # Inicialización del paquete
│   ├── cli.py                    # CLI principal unificado
│   ├── validator.py              # Validador de formatos
│   └── batch_converter.py        # Conversor en lotes
├── 📂 bloque-1/                  # Evaluaciones Bloque 1 (Semanas 1-5)
│   ├── canvas/                   # Bancos de preguntas Canvas
│   │   ├── banco-preguntas-bloque1.txt
│   │   └── generar_qti.py        # Wrapper compatibilidad
│   ├── caso-practico/            # Casos prácticos colaborativos
│   ├── datasets/                 # Datos para evaluaciones
│   └── rubricas/                 # Criterios de evaluación
├── 📂 bloque-2/                  # Evaluaciones Bloque 2 (Semanas 6-10)
│   └── [estructura idéntica]
└── 📂 bloque-3/                  # Evaluaciones Bloque 3 (Semanas 11-15)
    └── [estructura idéntica]
```

---

## 🔧 Workflow de Desarrollo

### Modificar Evaluaciones

1. **Editar preguntas:**
   ```bash
   # Editar banco de preguntas
   nano bloque-1/canvas/banco-preguntas-bloque1.txt
   
   # Validar formato
   eval-validate --bloque bloque-1
   
   # Generar QTI
   eval-qti --path bloque-1
   ```

2. **Actualizar casos prácticos:**
   ```bash
   # Modificar archivos en caso-practico/
   # Actualizar rúbricas correspondientes
   # Validar estructura completa
   eval-validate
   ```

### Flujo de Integración

1. **Validación previa:**
   ```bash
   eval-validate --verbose
   ```

2. **Conversión de prueba:**
   ```bash
   eval-batch --force --verbose
   ```

3. **Commit y push:**
   ```bash
   git add .
   git commit -m "update: evaluaciones bloque-X - [descripción]"
   git push origin main
   ```

---

## 🚀 Integración con txttoqti v0.3.0

Este sistema utiliza **txttoqti v0.3.0** con extensiones educativas:

### Características Principales

- **Auto-detección** de archivos de preguntas
- **Validación automática** de formato
- **Conversión inteligente** TXT → QTI Canvas
- **Manejo de errores** robusto
- **Compatibilidad retroactiva** con scripts existentes

### Comandos txttoqti Nativos

```bash
# Comando nativo (también disponible)
txttoqti-edu                    # Auto-detección global
txttoqti-edu --status          # Estado de todos los bloques
txttoqti-edu --path bloque-2   # Bloque específico
```

---

## 🔒 Seguridad y Políticas

### Control de Acceso

- **Repositorio privado** en GitHub/GitLab
- **Autenticación requerida** para clonado
- **Permisos granulares** por usuario
- **Auditoría de cambios** completa

### Buenas Prácticas

1. **Nunca compartir** fuera del contexto académico autorizado
2. **No subir** a repositorios públicos
3. **Usar ramas** para cambios experimentales
4. **Documentar cambios** en commits descriptivos
5. **Validar siempre** antes de commits

### Archivos Sensibles

El `.gitignore` excluye automáticamente:
- Respuestas privadas adicionales
- Configuraciones locales
- Archivos temporales de conversión
- Claves y secretos

---

## 📊 Métricas y Estadísticas

### Estado del Sistema

```bash
# Resumen completo
eval-qti --status

# Ejemplo de salida:
# 🎯 Sistema de Evaluaciones - Estado Global
# ==================================================
# 📁 BLOQUE-1
#    Archivos TXT: 1
#    Archivos ZIP: 1  
#    Estado: ✅ Actualizado
# 
# 📁 BLOQUE-2
#    Archivos TXT: 1
#    Archivos ZIP: 0
#    Estado: ⚠️  Pendiente
```

### Validación Detallada

```bash
# Análisis completo
eval-validate --verbose

# Reporta:
# - Formato de preguntas
# - Estructura de directorios
# - Integridad de archivos
# - Errores de sintaxis
```

---

## 🛠️ Resolución de Problemas

### Errores Comunes

#### txttoqti-edu no encontrado
```bash
# Solución: Reinstalar txttoqti
pip install git+https://github.com/julihocc/txttoqti.git@v0.3.0
```

#### Formato de preguntas incorrecto
```bash
# Usar validador para identificar errores
eval-validate --bloque bloque-X --verbose

# Formato esperado:
# Q1: ¿Pregunta aquí?
# A) Opción A
# B) Opción B
# C) Opción C
# D) Opción D
```

#### Permisos de acceso
```bash
# Verificar autenticación Git
git remote -v
ssh -T git@github.com
```

### Logs y Debugging

```bash
# Salida detallada para debugging
eval-batch --verbose --sequential

# Validación exhaustiva
eval-validate --verbose
```

---

## 📞 Soporte y Contacto

### Soporte Técnico
- **Repositorio:** Issues en GitHub privado
- **Email:** julio.hernandez@tec.mx
- **Documentación:** Este README y CLAUDE.md

### Actualizaciones
- **txttoqti:** Se actualiza automáticamente con `pip install -U`
- **Evaluaciones:** Pull requests en repositorio privado
- **Herramientas:** Versioning semántico en pyproject.toml

---

## 📋 Checklist de Configuración

- [ ] Repositorio clonado correctamente
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -e .`)
- [ ] Herramientas CLI funcionando (`eval-qti --help`)
- [ ] Validación exitosa (`eval-validate`)
- [ ] Primera conversión completada (`eval-qti --status`)
- [ ] Acceso a repositorio privado configurado
- [ ] Políticas de seguridad entendidas

---

**🎓 Sistema desarrollado para el Tecnológico de Monterrey**  
**Curso: Ciencia de Datos Aplicada al Fútbol**  
**Modalidad: Preparatoria - Modalidad Competencias**

*Documento confidencial - Distribución restringida*