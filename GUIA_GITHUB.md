# 📤 GUÍA: Subir Proyecto a GitHub (Repositorio Privado)

## ✅ Paso 1: Crear cuenta en GitHub (si no tienes)

1. Ve a https://github.com/signup
2. Completa el registro con:
   - Email
   - Contraseña
   - Username (ej: tu-nombre-usuario)
3. Verifica tu email
4. Personaliza tu perfil (opcional)

## ✅ Paso 2: Crear un nuevo repositorio en GitHub

1. Inicia sesión en GitHub
2. Haz clic en el **+ icon** (esquina superior derecha) → **New repository**
3. Completa los campos:
   - **Repository name**: `automatizacion-tareas` (o el nombre que prefieras)
   - **Description**: "Aplicación Flet para automatizar tareas: detectar duplicados, organizar archivos, etc."
   - **Visibility**: ⭕ **Private** (IMPORTANTE: Selecciona PRIVATE)
   - **Initialize this repository with**: Deja sin seleccionar
4. Haz clic en **Create repository**

## ✅ Paso 3: Instalar Git (Windows)

Si no tienes Git instalado:

1. Descarga desde: https://git-scm.com/download/win
2. Ejecuta el instalador
3. Selecciona todas las opciones por defecto
4. Completa la instalación

**Verificar que está instalado**:
```powershell
git --version
```

## ✅ Paso 4: Configurar Git (PRIMERA VEZ)

En PowerShell o CMD:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

**Ejemplo**:
```powershell
git config --global user.name "Ernes"
git config --global user.email "ernes@example.com"
```

## ✅ Paso 5: Inicializar Repositorio Local

Abre PowerShell en la carpeta del proyecto:

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git init
git add .
git commit -m "Primer commit: Proyecto inicial con app Flet funcional"
```

## ✅ Paso 6: Conectar con GitHub (IMPORTANTE)

### Opción A: Con HTTPS (más fácil)

1. Ve a tu repositorio en GitHub
2. Haz clic en **Code** (botón verde) → **HTTPS**
3. Copia la URL (ej: `https://github.com/tu-usuario/automatizacion-tareas.git`)
4. En PowerShell ejecuta:

```powershell
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
git branch -M main
git push -u origin main
```

**Nota**: Te pedirá credenciales. Usa:
- Usuario: tu email de GitHub
- Contraseña: Un token de acceso (ver Paso 7)

### Opción B: Con SSH (más seguro, requiere configuración)

1. Genera una clave SSH:
```powershell
ssh-keygen -t ed25519 -C "tu-email@example.com"
```

2. Cuando pregunte por el archivo, solo presiona Enter
3. Cuando pregunte por passphrase, solo presiona Enter
4. Ve a GitHub → Settings → SSH and GPG keys
5. Haz clic en "New SSH key"
6. Abre `C:\Users\tu-usuario\.ssh\id_ed25519.pub` (con Notepad)
7. Copia todo el contenido y pégalo en GitHub
8. Luego ejecuta:

```powershell
git remote add origin git@github.com:tu-usuario/automatizacion-tareas.git
git branch -M main
git push -u origin main
```

## ✅ Paso 7: Crear Token de Acceso (Para HTTPS)

1. Ve a GitHub → Settings (esquina superior derecha)
2. En el menú lateral: **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Haz clic en **Generate new token (classic)**
4. Completa:
   - **Note**: "Token para proyecto automatización-tareas"
   - **Expiration**: 90 days (o más)
   - **Scopes**: Selecciona `repo` (acceso completo a repositorios)
5. Haz clic en **Generate token**
6. **IMPORTANTE**: Copia el token y guárdalo en un lugar seguro
7. En PowerShell, cuando pida contraseña, pega el token

## ✅ Paso 8: Subir el Proyecto

Una vez configurado el remoto:

```powershell
git push -u origin main
```

Si todo va bien, verás:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## ✅ Paso 9: Verificar en GitHub

1. Abre tu repositorio en GitHub
2. Deberías ver todos tus archivos subidos
3. Verifica que sea **Private** (en Settings → Visibility)

## 📋 Comandos Útiles para el Futuro

**Después de hacer cambios en el código**:

```powershell
# Ver cambios
git status

# Agregar cambios
git add .

# Crear commit
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push origin main
```

**Ejemplo completo**:
```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git add .
git commit -m "Mejorar vista de duplicados con contador destacado"
git push origin main
```

## 🔒 Hacer el Repositorio Privado

1. Ve a tu repositorio en GitHub
2. **Settings** → **General**
3. Baja a **Danger Zone** → **Change repository visibility**
4. Selecciona **Make private**
5. Confirma escribiendo el nombre del repositorio
6. Haz clic en **I understand, make this repository private**

**IMPORTANTE**: Ya debería ser privado si lo creaste como Private en el Paso 2.

## 🔐 Agregar Colaboradores (Opcional)

Si quieres que otros accedan:

1. **Settings** → **Collaborators**
2. Haz clic en **Add people**
3. Busca por username o email
4. Selecciona el permiso (Pull, Push, Admin)
5. Envía la invitación

## ✨ Verificar que Todo Funcionó

```powershell
git remote -v
```

Deberías ver:
```
origin  https://github.com/tu-usuario/automatizacion-tareas.git (fetch)
origin  https://github.com/tu-usuario/automatizacion-tareas.git (push)
```

## 📞 Si Tienes Problemas

**Error: "fatal: not a git repository"**
```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git init
```

**Error: "Permission denied (publickey)"**
- Configura SSH correctamente (Opción B del Paso 6)
- O usa HTTPS con token (Opción A del Paso 6)

**Error: "The requested URL returned error: 403"**
- Verifica que el token sea válido
- Crea uno nuevo si expiró

---

**¿Preguntas?** Dime en qué paso te atascas y te ayudaré.
