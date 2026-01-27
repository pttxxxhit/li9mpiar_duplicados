# 🚀 Automatización de Tareas - Flet GUI

Aplicación de escritorio moderna construida con **Flet** para automatizar tareas comunes de gestión de archivos.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-0.80+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange.svg)

## ✨ Características

### 🗑️ Eliminar Archivos Duplicados
- **Detección inteligente** basada en hash MD5
- **Eliminación individual** o **en lote**
- **Diálogo de confirmación** para prevenir errores
- **Lista scrolleable** con detalles de duplicados
- **Contador visual** de archivos duplicados
- **Notificaciones** en tiempo real

### 📁 Organizar Archivos
- **Clasificación automática** por tipo de archivo
- **Subcarpetas inteligentes**:
  - 🖼️ Imágenes
  - 🎬 Videos
  - 📄 Documentos
  - 📊 Datasets
  - 📦 Comprimidos
  - 📋 Otros
- **Gestión de conflictos** (renombra automáticamente si existe)

### 🎨 Interfaz Moderna
- **Tema oscuro** optimizado
- **Navegación lateral** intuitiva
- **Diseño responsivo**
- **Iconos Material Design**
- **SnackBars** para feedback inmediato

## 🎯 Uso Rápido

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/automatizacion-tareas.git
cd automatizacion-tareas

# Crear entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# O en PowerShell
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar

**Versión básica** (2 vistas):
```powershell
python app.py
```

**Versión extendida** (7 vistas + fondo opcional):
```powershell
python main.py
```

**Con script de Windows**:
```powershell
ejecutar_app.bat
```

## 📊 Estructura del Proyecto

```
automatizacion-tareas/
├── app.py                      # App Flet principal (versión básica)
├── main.py                     # Versión extendida
├── borrar_duplicados.py        # Lógica de detección de duplicados
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── GUIA_GITHUB.md             # Guía completa GitHub
├── GITHUB_RAPIDO.md           # Inicio rápido GitHub
├── RESUMEN_MEJORAS.md         # Cambios implementados
├── MEJORAS_DUPLICADOS.md      # Detalles técnicos
├── PYCHARM_CONFIG.md          # Configuración PyCharm
├── .gitignore                 # Archivos ignorados
├── .venv/                     # Entorno virtual
└── test_duplicados/           # Carpeta de prueba
```

## 🛠️ Tecnologías

- **Flet** 0.80.4 - Framework GUI moderno
- **Python** 3.11+ - Lenguaje principal
- **Hashlib** - Detección de duplicados por MD5

## 📋 Funcionalidades Implementadas

### Vista: Eliminar Duplicados ✅
- [x] Seleccionar carpeta a escanear
- [x] Detección automática de duplicados
- [x] Mostrar contador de duplicados
- [x] Lista scrolleable con detalles
- [x] Eliminar archivos individuales
- [x] Eliminar todos con confirmación
- [x] Notificaciones de resultado
- [x] Rutas seleccionables

### Vista: Organizar Archivos ✅
- [x] Seleccionar carpeta a organizar
- [x] Crear subcarpetas automáticamente
- [x] Mover archivos por tipo
- [x] Evitar bucles recursivos
- [x] Renombrear duplicados
- [x] Notificación de resultado

### Próximas Funciones 🚧
- [ ] Redimensionar imágenes
- [ ] Convertir imágenes (PNG, JPG, WebP)
- [ ] Extraer audio de videos
- [ ] Fusionar PDFs
- [ ] Renombrar archivos en lote
- [ ] Barra de progreso para operaciones largas
- [ ] Exportar reporte de duplicados
- [ ] Vista previa de archivos

## 🚀 Cómo Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📸 Capturas de Pantalla

### Vista: Eliminar Duplicados
```
┌─────────────────────────────────────────────────┐
│ 🗑️ Eliminar Archivos Duplicados                │
│                                                 │
│ Encontra y elimina archivos duplicados          │
│ basándose en su contenido (hash MD5)            │
│                                                 │
│ [📁 Seleccionar carpeta] [Ruta seleccionada]  │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │ ⚠️ Se encontraron 6 archivos duplicados      ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ [Eliminar todos (6)]                           │
│                                                 │
│ ┌─ #1 Duplicado encontrado ─────────────────┐ │
│ │ Duplicado: C:\...\doc_copia1.txt          │ │
│ │ Original:  C:\...\doc.txt                 │ │
│ │                                 [🗑️]      │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ (más items...)                                  │
└─────────────────────────────────────────────────┘
```

## ⚙️ Requisitos Mínimos

- Windows 10 o superior
- Python 3.11+
- 50 MB de espacio en disco
- Conexión a internet (solo para instalar dependencias)

## 🔐 Privacidad y Seguridad

- ✅ Repositorio privado
- ✅ Los archivos se procesan localmente
- ✅ Sin conexión a internet requerida después de instalar
- ✅ Sin datos se envían a servidores externos

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Ernes** - Proyecto de automatización personal

## 📞 Contacto y Soporte

Para reportar bugs o sugerencias, abre un Issue en GitHub.

## 🙏 Agradecimientos

- [Flet](https://flet.dev/) - Framework GUI excelente
- [Python](https://www.python.org/) - Lenguaje poderoso
- Community de open source

---

**¡Disfruta automatizando tus tareas!** 🚀
