# 📋 COPIAR Y PEGAR - COMANDOS LISTOS

## 🎯 Usa estos comandos exactos (copia y pega en PowerShell)

### PASO 1: Configurar Git (PRIMERA VEZ SOLO)

```powershell
git config --global user.name "Tu Nombre Aqui"
git config --global user.email "tuemail@gmail.com"
```

**Ejemplo real**:
```powershell
git config --global user.name "Ernes"
git config --global user.email "ernes@gmail.com"
```

### PASO 2: Ir a la carpeta del proyecto

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
```

### PASO 3: Inicializar repositorio

```powershell
git init
git add .
git commit -m "Respaldo inicial: App Flet completa"
git branch -M main
```

### PASO 4: Agregar remoto de GitHub

**IMPORTANTE**: Reemplaza `tu-usuario` con TU USERNAME de GitHub

```powershell
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
```

**Ejemplo real**:
```powershell
git remote add origin https://github.com/ernes2024/automatizacion-tareas.git
```

### PASO 5: Subir a GitHub

```powershell
git push -u origin main
```

**Cuando pida credenciales**:
- Usuario: Tu email de GitHub
- Contraseña: Tu TOKEN (copiar de GitHub Settings)

---

## 🔄 COMANDOS PARA FUTUROS CAMBIOS

### Después de cambiar código

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git add .
git commit -m "Descripción del cambio aquí"
git push origin main
```

**Ejemplos**:
```powershell
git commit -m "Agregar vista para redimensionar imágenes"
git commit -m "Corregir bug en eliminación de duplicados"
git commit -m "Mejorar interfaz con nuevos iconos"
```

---

## 🔒 GENERAR TOKEN (SI NECESITAS)

1. Abre: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Dale un nombre: "CLI Token"
4. Marca: `repo`
5. Click "Generate token"
6. **COPIA** el token (no lo verás de nuevo)
7. Usa el token como contraseña en `git push`

---

## ✅ VERIFICAR QUE FUNCIONA

```powershell
git remote -v
```

Deberías ver:
```
origin  https://github.com/tu-usuario/automatizacion-tareas.git (fetch)
origin  https://github.com/tu-usuario/automatizacion-tareas.git (push)
```

---

## 🆘 SI ALGO FALLA

### Error: "Permission denied"
```powershell
git remote remove origin
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
git push -u origin main
```

### Error: "fatal: not a git repository"
```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git init
git add .
git commit -m "Respaldo inicial"
```

### Error: "Repository not found"
- Verifica que el repositorio exista en GitHub
- Verifica que la URL sea correcta
- Copia URL directamente de GitHub (botón "Code")

---

## 📋 CHECKLIST PASO A PASO

- [ ] Tengo cuenta en GitHub (https://github.com)
- [ ] Creé repositorio privado en GitHub
- [ ] Tengo Git instalado (`git --version`)
- [ ] Abrí PowerShell en: `C:\Users\ernes\Desktop\proyectofinal`
- [ ] Ejecuté: `git config --global ...` (configurar)
- [ ] Ejecuté: `git init` (inicializar)
- [ ] Ejecuté: `git add .` (agregar archivos)
- [ ] Ejecuté: `git commit -m "..."` (crear commit)
- [ ] Ejecuté: `git branch -M main` (crear rama)
- [ ] Ejecuté: `git remote add origin ...` (conectar con GitHub)
- [ ] Ejecuté: `git push -u origin main` (subir a GitHub)
- [ ] Verifiqué en https://github.com/tu-usuario/automatizacion-tareas

---

## 🎯 PLANTILLA COMPLETA (COPIAR Y PEGAR)

Si quieres hacerlo todo de una vez:

```powershell
# Paso 1: Configurar Git (si es la primera vez)
git config --global user.name "Ernes"
git config --global user.email "ernes@gmail.com"

# Paso 2: Ir a la carpeta
cd C:\Users\ernes\Desktop\proyectofinal

# Paso 3: Inicializar y hacer commit
git init
git add .
git commit -m "Respaldo inicial: App Flet completa"
git branch -M main

# Paso 4: Conectar con GitHub (CAMBIA tu-usuario)
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git

# Paso 5: Subir a GitHub
git push -u origin main

# Paso 6: Verificar
git remote -v
```

**Nota**: Cambia `tu-usuario` por tu username real de GitHub

---

## 📝 NOMBRES DE COMMIT SUGERIDOS

Usa estos para describir cambios:

```powershell
# Para agregaciones
git commit -m "Agregar vista para redimensionar imágenes"

# Para correcciones
git commit -m "Corregir bug en eliminación de duplicados"

# Para mejoras
git commit -m "Mejorar interfaz con nuevos colores"

# Para refactorización
git commit -m "Refactorizar código de detección de duplicados"

# Para documentación
git commit -m "Actualizar README con nuevas instrucciones"
```

---

## 🔐 MANTENER SEGURIDAD

**NUNCA hagas esto**:
- ❌ No compartas tu token
- ❌ No copies token en código
- ❌ No guardes token en archivos de texto

**SÍ haz esto**:
- ✅ Copia token en momento de uso
- ✅ Regenera token si lo compartiste
- ✅ Usa tokens con expiración

---

## ✨ ¡LISTO PARA COPIAR Y PEGAR!

Todos los comandos están listos para usar.
Solo cambia `tu-usuario` por tu username de GitHub.

**¿Preguntas?** Consulta `TROUBLESHOOTING.md`
