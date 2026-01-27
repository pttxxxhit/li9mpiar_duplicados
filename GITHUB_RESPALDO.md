# 📤 RESPALDAR EN GITHUB - INSTRUCCIONES COMPLETAS

## 🎯 OBJETIVO
Crear un respaldo privado de tu proyecto en GitHub para:
- ✅ Proteger tu código
- ✅ Tener historial de cambios
- ✅ Acceder desde cualquier lugar
- ✅ Colaborar con otros (opcional)

## 📋 CHECKLIST ANTES DE EMPEZAR

- [ ] Tienes una cuenta en GitHub (https://github.com/signup)
- [ ] Tienes Git instalado (https://git-scm.com/download/win)
- [ ] Estás en la carpeta del proyecto

## ⚡ OPCIÓN RÁPIDA (Recomendada - 5 minutos)

### 1. Crear repo en GitHub
1. Ve a: https://github.com/new
2. Nombre: `automatizacion-tareas`
3. **IMPORTANTE**: Selecciona **PRIVATE** 🔒
4. Crea el repo

### 2. Configurar Git
```powershell
# Abre PowerShell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 3. Subir proyecto
```powershell
# En PowerShell, en la carpeta del proyecto
cd C:\Users\ernes\Desktop\proyectofinal

git init
git add .
git commit -m "Respaldo inicial: App Flet con duplicados y organización"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/automatizacion-tareas.git
git push -u origin main
```

Cambia `TU-USUARIO` por tu usuario de GitHub.

### 4. Proporcionar credenciales
Cuando pida usuario y contraseña:
- **Usuario**: tu email de GitHub
- **Contraseña**: Tu token (ver Paso 5 abajo)

### 5. Generar Token
1. Ve a: https://github.com/settings/tokens
2. Click en **Generate new token (classic)**
3. Marca: `repo`
4. Genera el token
5. **COPIA** el token
6. Úsalo como contraseña en el paso 3

## 📚 OPCIÓN DETALLADA (Con explicaciones)

Ver el archivo: **GUIA_GITHUB.md**

## ✅ VERIFICAR QUE FUNCIONÓ

1. Abre: `https://github.com/tu-usuario/automatizacion-tareas`
2. Deberías ver:
   - ✅ Todos tus archivos (app.py, main.py, etc.)
   - ✅ Estado: **Private** 🔒
   - ✅ Rama: **main**

## 🔄 FUTURO: SUBIR CAMBIOS

Cada vez que hagas cambios:

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git add .
git commit -m "Descripción de cambios"
git push origin main
```

**Ejemplos**:
```powershell
git commit -m "Agregar vista para redimensionar imágenes"
git commit -m "Corregir bug en eliminación de duplicados"
git commit -m "Mejorar interfaz con nuevos colores"
```

## 📝 ARCHIVOS DE AYUDA EN TU PROYECTO

- `GITHUB_RAPIDO.md` - Guía rápida (este archivo)
- `GUIA_GITHUB.md` - Guía detallada con todas las opciones
- `README.es.md` - Descripción del proyecto para GitHub
- `.gitignore` - Archivos que NO se suben

## 🔐 SEGURIDAD

**Tu repositorio es PRIVADO**, solo tú puedes ver:
- El código
- Los commits
- El historial

Si quieres que otros vean:
1. Ve a GitHub Settings
2. "Collaborators" → "Add people"
3. Busca y selecciona a quien quieres agregar

## ❌ ERRORES COMUNES

| Error | Solución |
|-------|----------|
| "fatal: not a git repository" | Asegúrate de estar en la carpeta correcta |
| "Permission denied" | Verifica el token, créa uno nuevo |
| "could not read Username" | Usa el token como contraseña |
| "Repository not found" | Verifica que el repo exista en GitHub |

## 🎓 APRENDER GIT

Si quieres aprender más sobre Git:
- https://git-scm.com/book/es/v2
- https://github.com/skills/introduction-to-github

## 💡 TIPS ÚTILES

1. **Haz commits frecuentes**: No esperes a terminar todo para hacer backup
2. **Usa mensajes descriptivos**: Describe qué cambió y por qué
3. **Protege tu token**: Nunca lo compartas públicamente
4. **Revisa los cambios**: Usa `git status` antes de hacer push

## 🚀 ¡LISTO!

Sigue los pasos de la opción rápida y en 5 minutos tu proyecto estará respaldado en GitHub de forma privada.

---

**¿Necesitas ayuda?**
- Consulta GUIA_GITHUB.md
- Abre un issue en GitHub
- Revisa la documentación oficial

**¡Éxito con tu proyecto!** 🎉
