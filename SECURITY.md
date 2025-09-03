# Políticas de Seguridad - Sistema de Evaluaciones

## 🔐 Confidencialidad del Contenido

Este repositorio contiene **material evaluativo confidencial** para el curso "Ciencia de Datos Aplicada al Fútbol" del Tecnológico de Monterrey:

- ✅ **Bancos de preguntas** con respuestas correctas marcadas
- ✅ **Casos prácticos** con soluciones modelo completas  
- ✅ **Rúbricas de evaluación** con criterios específicos
- ✅ **Datasets educativos** diseñados para evaluación

## 👥 Control de Acceso

### Personal Autorizado

**ACCESO RESTRINGIDO** únicamente a:
- Profesores del curso asignados oficialmente
- Coordinadores académicos del área
- Personal de soporte técnico autorizado por la coordinación
- Desarrolladores del sistema (con NDA institucional)

### Niveles de Permisos

| Rol | Lectura | Escritura | Administración |
|-----|---------|-----------|----------------|
| Profesor Titular | ✅ | ✅ | ❌ |
| Profesor Adjunto | ✅ | ❌ | ❌ |
| Coordinador | ✅ | ✅ | ✅ |
| Soporte Técnico | ✅ | ❌ | ❌ |

## 🚫 Restricciones de Uso

### Prohibido Estrictamente

- ❌ **Compartir** contenido fuera del contexto académico autorizado
- ❌ **Publicar** en repositorios públicos (GitHub, GitLab, etc.)
- ❌ **Distribuir** a estudiantes antes de evaluaciones
- ❌ **Copiar** para uso en otras instituciones sin autorización
- ❌ **Modificar** sin coordinación académica previa

### Uso Permitido

- ✅ **Generar evaluaciones** Canvas para el curso oficial
- ✅ **Adaptar preguntas** para contextos específicos del grupo
- ✅ **Crear variaciones** de casos prácticos manteniendo confidencialidad
- ✅ **Desarrollar herramientas** de apoyo académico

## 🔒 Medidas de Seguridad Técnica

### Repositorio

- **Privado** en GitHub/GitLab institucional
- **Autenticación 2FA** requerida para todos los colaboradores
- **Auditoría completa** de accesos y modificaciones
- **Backups automáticos** en infraestructura institucional

### Acceso Local

- **Entornos virtuales** obligatorios para desarrollo
- **Claves SSH** con passphrase para autenticación
- **Archivos sensibles** excluidos via `.gitignore`
- **Encriptación** de dispositivos locales recomendada

## 📋 Protocolo de Manejo

### Clonado Inicial

```bash
# Solo usuarios autorizados con acceso SSH configurado
git clone git@github.com:tec-monterrey/ciencia-datos-futbol-evaluaciones.git

# Verificar configuración de usuario institucional
git config user.email "usuario@tec.mx"
```

### Trabajo Diario

1. **Siempre** trabajar en ramas feature para cambios importantes
2. **Validar** contenido antes de commits (`eval-validate`)
3. **Documentar** cambios con mensajes descriptivos
4. **Revisar** logs de acceso periódicamente

### Emergencias

En caso de **exposición accidental** de contenido:

1. **Contacto inmediato** a coordinación académica
2. **Rotación** de preguntas comprometidas
3. **Análisis** de impacto en evaluaciones programadas
4. **Documentación** del incidente para prevención futura

## 🛡️ Medidas Preventivas

### Configuración `.gitignore`

El repositorio incluye exclusiones automáticas para:

```gitignore
# Archivos sensibles adicionales
**/respuestas-privadas/
**/keys/
**/soluciones-completas/
local_config.py
.secrets
```

### Validación Pre-commit

```bash
# Antes de cada commit
eval-validate --verbose
git diff --staged  # Revisar cambios staged
```

### Monitoreo de Integridad

```bash
# Verificación periódica del estado
eval-qti --status
find . -name "*.zip" -mtime -7  # Archivos recientes
```

## 🚨 Reportar Incidentes de Seguridad

### Canales de Reporte

- **Email urgente:** seguridad.academica@tec.mx
- **Issues privados:** En repositorio institucional
- **Teléfono:** Extensión de emergencias TI

### Información Requerida

1. **Descripción** del incidente o vulnerabilidad
2. **Pasos** para reproducir el problema
3. **Impacto potencial** en evaluaciones
4. **Archivos afectados** (sin incluir contenido sensible)
5. **Fecha y hora** del descubrimiento

## 📚 Capacitación y Concienciación

### Inducción Obligatoria

Todo personal con acceso debe completar:

- **Sesión de seguridad** informática institucional
- **Capacitación específica** en manejo de evaluaciones
- **Firma de acuerdo** de confidencialidad
- **Prueba de conocimientos** sobre políticas

### Actualizaciones Regulares

- **Reuniones semestrales** de revisión de políticas
- **Comunicados** sobre nuevas amenazas o procedimientos
- **Auditorías anuales** de cumplimiento

## ✅ Checklist de Cumplimiento

### Para Usuarios Nuevos

- [ ] Acceso autorizado por coordinación académica
- [ ] Configuración 2FA en GitHub/GitLab
- [ ] Clave SSH con passphrase configurada
- [ ] Usuario Git con email institucional
- [ ] Entorno virtual configurado correctamente
- [ ] Lectura completa de políticas de seguridad
- [ ] Firma de acuerdo de confidencialidad

### Para Uso Continuo

- [ ] Validación de contenido antes de commits
- [ ] Uso exclusivo en contexto académico autorizado
- [ ] Actualización regular de herramientas (txttoqti, etc.)
- [ ] Backup personal en infraestructura institucional únicamente
- [ ] Reporte inmediato de anomalías o incidentes

---

## 📞 Contactos de Seguridad

| Rol | Contacto | Horario |
|-----|----------|---------|
| Coordinador Académico | coord.cienciadatos@tec.mx | Hábil 8-18h |
| Soporte Técnico | soporte.evaluaciones@tec.mx | 24/7 |
| Seguridad Informática | seguridad@tec.mx | Emergencias 24/7 |
| Desarrollador Principal | julio.hernandez@tec.mx | Hábil 9-17h |

---

**🏛️ Tecnológico de Monterrey - Campus [Campus]**  
**Documento vigente desde:** Fecha de creación del repositorio  
**Última actualización:** Automática con cada versión  
**Próxima revisión:** Semestre académico siguiente

*Este documento es de carácter confidencial y su distribución está restringida al personal académico autorizado del Tecnológico de Monterrey.*