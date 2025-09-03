# Guía de Migración: evaluaciones → Repositorio Privado

## 🎯 Objetivo de la Migración

Separar el contenido evaluativo sensible del repositorio principal del curso para:

- 🔒 **Seguridad**: Contenido confidencial en repositorio privado
- 🚀 **Independencia**: Dependencias y versionado específicos  
- 👥 **Control de acceso**: Permisos granulares para personal autorizado
- 📦 **Mantenibilidad**: Herramientas especializadas para evaluaciones

## ⚡ Migración Completada

### ✅ Pasos Ejecutados

1. **Extracción de historial completo** con `git subtree split`
2. **Creación de repositorio independiente** con historial preservado
3. **Configuración de Python package** con CLI especializado
4. **Herramientas CLI avanzadas** para gestión evaluativa
5. **Documentación completa** incluyendo políticas de seguridad

### 📊 Estadísticas de Migración

- **Commits preservados**: 508 commits completos del directorio evaluaciones
- **Reducción de código**: 96.7% gracias a txttoqti v0.3.0
- **Herramientas nuevas**: 3 CLIs especializados (`eval-qti`, `eval-validate`, `eval-batch`)
- **Archivos migrados**: 596KB de contenido evaluativo

## 🏗️ Configuración Post-Migración

### En el Repositorio Principal

El repositorio principal ahora usará **git submodule** para integrar evaluaciones:

```bash
# 1. Eliminar directorio evaluaciones actual
cd /ruta/al/repo/principal
git rm -r evaluaciones/

# 2. Agregar como submodule privado  
git submodule add <url-repo-privado> evaluaciones

# 3. Actualizar .gitmodules (automático)
# 4. Commit de la migración
git commit -m "migrate: evaluaciones to private submodule repository"
```

### Actualización de CLAUDE.md

```markdown
# Evaluaciones (Repositorio Privado)
git submodule update --remote evaluaciones  # Actualizar evaluaciones  
cd evaluaciones && pip install -e .          # Instalar dependencias

# Comandos evaluaciones
eval-qti --status          # Estado global
eval-qti --convert-all     # Conversión masiva  
eval-validate             # Validación completa
```

## 🔄 Workflow Actualizado

### Para Instructores

#### Acceso Inicial

```bash
# 1. Clonar repositorio principal CON submodules
git clone --recurse-submodules <url-repo-principal>

# 2. Configurar evaluaciones
cd evaluaciones
pip install -e .

# 3. Verificar acceso
eval-qti --status
```

#### Trabajo Diario

```bash
# Actualizar contenido del curso (repo principal)
git pull origin main

# Actualizar evaluaciones (submodule privado)
git submodule update --remote evaluaciones

# Generar QTI actualizado
cd evaluaciones
eval-qti --convert-all
```

### Para Desarrolladores

#### Modificar Evaluaciones

```bash
# 1. Trabajar en el submodule
cd evaluaciones
git checkout main
git pull origin main

# 2. Crear rama feature
git checkout -b feature/nuevo-banco-preguntas

# 3. Hacer cambios y validar
# ... editar archivos ...
eval-validate --verbose

# 4. Commit y push al repo privado
git add .
git commit -m "feat: add nuevas preguntas bloque-2"
git push origin feature/nuevo-banco-preguntas

# 5. Actualizar referencia en repo principal
cd ..  # volver al repo principal
git add evaluaciones
git commit -m "update: evaluaciones submodule pointer"
```

## 🛠️ Herramientas Especializadas

### CLI Principal (`eval-qti`)

Reemplaza los scripts individuales con interfaz unificada:

```bash
# Antes (múltiples scripts)
cd evaluaciones/bloque-1/canvas && python generar_qti.py
cd evaluaciones/bloque-2/canvas && python generar_qti.py
cd evaluaciones/bloque-3/canvas && python generar_qti.py

# Después (comando unificado)
eval-qti --convert-all
```

### Validador (`eval-validate`)

Nueva herramienta para verificar integridad:

```bash
# Validar formato de todas las preguntas
eval-validate

# Validar bloque específico con detalles
eval-validate --bloque bloque-2 --verbose

# Output ejemplo:
# 🔍 Validador de Evaluaciones
# ==============================
# 📁 Validando BLOQUE-2...
# ✅ BLOQUE-2: Sin errores detectados
```

### Conversor en Lotes (`eval-batch`)

Procesamiento eficiente de múltiples bloques:

```bash
# Conversión paralela (por defecto)
eval-batch

# Conversión secuencial para debugging
eval-batch --sequential --verbose

# Bloques específicos con fuerza
eval-batch --bloques bloque-1 bloque-3 --force
```

## 📋 Resolución de Problemas

### Problemas Comunes

#### Submodule no se actualiza

```bash
# Forzar actualización del submodule
git submodule update --remote --force evaluaciones
```

#### Permisos de acceso al repo privado

```bash
# Verificar configuración SSH
ssh -T git@github.com

# Configurar acceso específico para submodule
cd evaluaciones
git remote set-url origin git@github.com:org/evaluaciones-privado.git
```

#### txttoqti no encontrado

```bash
# Reinstalar dependencias en evaluaciones
cd evaluaciones
pip install -e . --force-reinstall
```

### Debugging Avanzado

```bash
# Verificar estado completo
eval-qti --status --verbose

# Validar todo el contenido
eval-validate --verbose

# Información de submodule
git submodule status
```

## 🚀 Ventajas Post-Migración

### Seguridad Mejorada

- ✅ **Repositorio privado** con control de acceso granular
- ✅ **Auditoría completa** de cambios en evaluaciones
- ✅ **Separación de contextos** (curso público, evaluaciones privadas)

### Funcionalidad Expandida

- ✅ **Herramientas CLI especializadas** para evaluaciones
- ✅ **Validación automática** de formato y contenido
- ✅ **Procesamiento en lotes** eficiente
- ✅ **Integración txttoqti v0.3.0** con zero mantenimiento

### Mantenibilidad

- ✅ **Versionado independiente** de evaluaciones
- ✅ **Dependencias específicas** sin conflictos
- ✅ **Documentación dedicada** para uso evaluativo
- ✅ **Backup y recovery** independiente

## 🎓 Casos de Uso

### Instructor Nuevo

```bash
# Setup completo en 3 comandos
git clone --recurse-submodules <repo-curso>
cd evaluaciones && pip install -e .
eval-qti --status  # ✅ Todo listo
```

### Actualización de Evaluaciones

```bash
# Modificar preguntas
nano bloque-1/canvas/banco-preguntas-bloque1.txt
eval-validate  # Verificar formato
eval-qti --path bloque-1  # Generar QTI
```

### Preparación Semestre

```bash
# Conversión masiva con validación
eval-validate --verbose
eval-batch --force --verbose
eval-qti --status  # Verificar estado final
```

## 📞 Soporte Post-Migración

### Documentación Actualizada

- **README-PRIVADO.md**: Guía completa del repo evaluaciones
- **SECURITY.md**: Políticas de confidencialidad
- **CLAUDE.md**: Instrucciones actualizadas para el repo principal

### Recursos de Ayuda

- 📧 **Email**: julio.hernandez@tec.mx
- 🐛 **Issues**: Repositorio privado de evaluaciones
- 📚 **Wiki**: Documentación interna institucional

---

## ✅ Checklist de Migración Completada

- [x] Historial extraído con git subtree split
- [x] Repositorio independiente creado
- [x] Python package configurado (pyproject.toml)
- [x] CLIs especializados desarrollados
- [x] Documentación completa creada
- [x] Políticas de seguridad establecidas
- [x] Instrucciones de integración documentadas
- [x] Casos de uso y ejemplos incluidos

**🎯 Migración lista para implementación en producción**

La separación de evaluaciones en repositorio privado está **completamente preparada** y lista para ser implementada con los equipos de desarrollo e instruccionales.

---

*Documento técnico - Migración ejecutada el 2025-09-03*  
*Sistema: Ciencia de Datos Aplicada al Fútbol - Tecnológico de Monterrey*