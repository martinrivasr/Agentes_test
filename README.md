# Agentes Test - Limpieza de Páginas HTML

Repositorio para limpiar y optimizar páginas HTML capturadas con SingleFile.

## 📁 Estructura del Proyecto

```
Agentes_test/
├── original/          # Páginas HTML sin limpiar (capturadas con SingleFile)
├── clean/             # Páginas HTML limpias y optimizadas (output)
├── scripts/           # Scripts de automatización
│   ├── clean_html.py      # Limpia archivos HTML
│   └── update_links.py    # Actualiza links internos
└── README.md          # Este archivo
```

## 🚀 Proceso de Limpieza

### Paso 1: Subir Páginas Originales

1. Guarda todas tus páginas capturadas en la carpeta `/original/`
2. Puedes subirlas en **batches** (grupos) - no es necesario tener todas las 50 a la vez
3. Mantén la estructura de carpetas si las páginas tienen subdirectorios

**Desde VS Code:**
```bash
# Añadir archivos
git add original/

# Commit
git commit -m "Add batch of original HTML pages"

# Push
git push origin main
```

### Paso 2: Ejecutar Script de Limpieza

El script `clean_html.py` procesa todas las páginas en `/original/` y genera versiones limpias en `/clean/`.

```bash
# Desde la carpeta del repositorio
python3 scripts/clean_html.py
```

**¿Qué hace el script?**
- ✓ Remueve iframes de tracking (HubSpot, Evernote, etc.)
- ✓ Elimina atributos innecesarios (data-evernote-id, data-wf-*, etc.)
- ✓ Consolida todos los bloques CSS en uno solo
- ✓ Remueve comentarios de SingleFile
- ✓ Mantiene TODO el contenido visible intacto
- ✓ Reduce el tamaño del archivo (~9-10%)

### Paso 3: Actualizar Links Internos

El script `update_links.py` asegura que todos los enlaces entre páginas funcionen correctamente.

```bash
# Desde la carpeta del repositorio
python3 scripts/update_links.py
```

**¿Qué hace el script?**
- ✓ Encuentra todos los enlaces `<a href="...">` internos
- ✓ Actualiza rutas para que apunten a `/clean/` en vez de `/original/`
- ✓ Mantiene enlaces externos sin cambios
- ✓ Asegura que la navegación entre páginas funcione

## 📝 Workflow Completo (Proceso Recomendado)

### Opción A: Todo de una vez (50 páginas)

```bash
# 1. Subir todas las páginas a /original/ desde VS Code
git add original/
git commit -m "Add all 50 original pages"
git push origin main

# 2. Claude ejecuta los scripts de limpieza
python3 scripts/clean_html.py
python3 scripts/update_links.py

# 3. Commit y push de páginas limpias
git add clean/
git commit -m "Add cleaned and linked pages"
git push origin main
```

### Opción B: Por batches (Recomendado para probar primero)

```bash
# Batch 1: 10 páginas
git add original/pagina1.html original/pagina2.html ... original/pagina10.html
git commit -m "Add batch 1: pages 1-10"
git push origin main

# Claude limpia el batch 1
python3 scripts/clean_html.py
python3 scripts/update_links.py

# Verificar que todo funciona bien

# Batch 2: Siguientes 10 páginas
# ... repetir proceso
```

## 💡 Preguntas Frecuentes

### ¿Puedo subir las páginas desde VS Code?
**Sí**, usa `git push` normalmente desde VS Code. Cuando subas archivos nuevos, yo haré `git pull` para verlos.

### ¿Necesitas las 50 páginas completas?
**No**, puedes subirlas en **batches**. Esto es mejor porque:
- Puedes probar el proceso con pocas páginas primero
- Más fácil de trackear si algo sale mal
- No saturas el repositorio de golpe

### ¿Los links entre páginas funcionarán?
**Sí**, el script `update_links.py` se encarga de actualizar todos los enlaces internos automáticamente.

### ¿Qué pasa si las páginas están en subcarpetas?
El script mantiene la estructura de carpetas. Si tienes:
```
original/
  ├── seccion1/page1.html
  └── seccion2/page2.html
```

Generará:
```
clean/
  ├── seccion1/page1.html
  └── seccion2/page2.html
```

## 🔧 Uso Avanzado

### Limpiar un directorio específico
```bash
python3 scripts/clean_html.py /ruta/entrada /ruta/salida
```

### Actualizar links en directorio específico
```bash
python3 scripts/update_links.py /ruta/directorio
```

## 📊 Estadísticas de Limpieza

Por cada archivo procesado, verás:
- Número de iframes removidos
- Atributos eliminados
- Clases removidas
- Bloques CSS consolidados
- Reducción de tamaño (MB y %)

**Ejemplo de output:**
```
Limpiando: original/page1.html
  ✓ 3 iframes removidos
  ✓ 1257 atributos removidos
  ✓ 1139 clases removidas
  ✓ 20 bloques CSS consolidados en 1
  ✓ Tamaño: 5.75MB → 5.20MB (9.5% reducción)
  ✓ Guardado en: clean/page1.html
```

## 🎯 Próximos Pasos

1. **Sube tu primer batch** de páginas a `/original/`
2. **Avísame cuando esté listo** para que ejecute los scripts
3. **Verifica que las páginas limpias** funcionen correctamente
4. **Repite el proceso** con más batches hasta completar las 50

¿Listo para empezar? ¡Sube tu primer batch! 🚀
