# 🔒 RESPALDAR EN GITHUB - GUÍA RÁPIDA

## 📋 PASOS RÁPIDOS (5-10 minutos)

### 1️⃣ Crear Repositorio en GitHub

1. Abre: https://github.com/new
2. Nombre: `automatizacion-tareas`
3. Descripción: "App Flet para eliminar duplicados y organizar archivos"
4. **IMPORTANTE**: Selecciona **PRIVATE** ⭕
5. Haz clic en **Create repository**

### 2️⃣ Instalar Git (si no lo tienes)

1. Descarga: https://git-scm.com/download/win
2. Ejecuta el instalador
3. Sigue los pasos por defecto
4. Reinicia tu computadora

**Verificar**:
```powershell
git --version
```

### 3️⃣ Configurar Git

Abre PowerShell y ejecuta:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

**Ejemplo**:
```powershell
git config --global user.name "Ernes"
git config --global user.email "ernes@gmail.com"
```

### 4️⃣ Subir el Proyecto

Abre PowerShell en la carpeta `C:\Users\ernes\Desktop\proyectofinal`:

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
```

Luego ejecuta estos comandos (reemplaza TU-USUARIO):

```powershell
git init
git add .
git commit -m "Primer respaldo: App Flet funcional"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/automatizacion-tareas.git
git push -u origin main
```

**Cuando pida usuario y contraseña**:
- Usuario: tu email de GitHub
- Contraseña: Tu token de acceso (ver Paso 5)

### 5️⃣ Crear Token de Acceso

1. Ve a: https://github.com/settings/tokens
2. Haz clic en **Generate new token (classic)**
3. Dale un nombre: "GitHub CLI"
4. Expiration: 90 days
5. Marca: `repo` (acceso completo)
6. Haz clic en **Generate token**
7. **COPIA EL TOKEN** (no podrás verlo de nuevo)
8. Úsalo como contraseña en el paso 4

## ✅ ¿Cómo sé que funcionó?

1. Abre: https://github.com/tu-usuario/automatizacion-tareas
2. Deberías ver todos tus archivos:
   - ✅ app.py
   - ✅ main.py
   - ✅ borrar_duplicados.py
   - ✅ README.md
   - ✅ requirements.txt
   - ✅ .gitignore
   - etc.

3. En la esquina superior izquierda debe decir **Private** 🔒

## 📤 En el futuro (después de cambios)

Cada vez que hagas cambios, ejecuta:

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git add .
git commit -m "Descripción de lo que cambió"
git push origin main
```

## ❓ PROBLEMAS COMUNES

**Error: "fatal: not a git repository"**
```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git init
```

**Error: "could not read Username"**
- Crea un token: https://github.com/settings/tokens
- Usa el token como contraseña (en lugar de tu contraseña)

**Error: "Permission denied"**
- Verifica que el repositorio sea privado en GitHub Settings
- Verifica que tengas acceso de escritura

## 🚀 ALTERNATIVA: Script Automático

Si tienes Git instalado, simplemente ejecuta:

```powershell
.\subir_github.bat
```

(Edita el archivo primero y cambia: `tu-usuario-github` y `automatizacion-tareas`)

## 📚 Recursos

- Documentación completa: `GUIA_GITHUB.md`
- GitHub Help: https://docs.github.com

---

**¿Listo?** ¡Sigue los 5 pasos y tu proyecto estará respaldado! 🎉
