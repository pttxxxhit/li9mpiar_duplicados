# 🆘 SOLUCIÓN DE PROBLEMAS - GITHUB BACKUP

## ❌ Errores Comunes y Soluciones

### Error 1: "fatal: not a git repository"

**Problema**: Git no reconoce la carpeta como repositorio

**Solución**:
```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git init
git add .
git commit -m "Respaldo inicial"
```

---

### Error 2: "Permission denied (publickey)"

**Problema**: No puede conectar con GitHub (SSH)

**Soluciones**:

#### Opción A: Usar HTTPS en lugar de SSH
```powershell
# Si ya agregaste origin, cambia:
git remote remove origin
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
git push -u origin main
```

#### Opción B: Configurar SSH correctamente
```powershell
# Generar nueva clave SSH
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Simplemente presiona Enter en los prompts
# Luego agrega la clave pública a GitHub:
# 1. Ve a GitHub Settings → SSH keys
# 2. New SSH key
# 3. Copia contenido de: C:\Users\tu-usuario\.ssh\id_ed25519.pub
# 4. Pega en GitHub
```

---

### Error 3: "could not read Username for 'https://github.com': No such file or directory"

**Problema**: Git pide credenciales pero no las acepta

**Solución**:
```powershell
# Usa un token en lugar de contraseña
# 1. Genera token en GitHub: https://github.com/settings/tokens
# 2. Cuando Git pida contraseña, pega el token

# Si sigue sin funcionar, guarda credenciales:
git config --global credential.helper wincred

# Intenta push de nuevo
git push -u origin main
```

---

### Error 4: "The requested URL returned error: 403"

**Problema**: No tienes permisos o token inválido

**Solución**:
```powershell
# El token expiró, crea uno nuevo:
# 1. Ve a: https://github.com/settings/tokens
# 2. Genera nuevo token (copia y guarda en lugar seguro)
# 3. Cuando Git pida contraseña, pega el token nuevo

# O borra credenciales guardadas y vuelve a intentar:
git config --global --unset credential.helper
git push -u origin main
```

---

### Error 5: "fatal: remote origin already exists"

**Problema**: Ya existe una conexión remota

**Solución**:
```powershell
# Opción A: Reemplaza el origin existente
git remote remove origin
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
git push -u origin main

# Opción B: Verifica qué hay
git remote -v
```

---

### Error 6: "fatal: 'origin' does not appear to be a 'git' repository"

**Problema**: La URL del repositorio es incorrecta

**Solución**:
```powershell
# Verifica la URL:
git remote -v

# Si es incorrecta, corrígela:
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/automatizacion-tareas.git

# Nota: Reemplaza TU-USUARIO con tu username real
```

---

## ⚠️ Problemas en Windows

### PowerShell no reconoce git

**Problema**: Escribes `git` y PowerShell no lo reconoce

**Soluciones**:

#### Opción 1: Reinstalar Git
```powershell
# 1. Descarga: https://git-scm.com/download/win
# 2. Ejecuta el instalador
# 3. Marca "Add Git to PATH"
# 4. Completa la instalación
# 5. Reinicia PowerShell
```

#### Opción 2: Usa la ruta completa
```powershell
"C:\Program Files\Git\bin\git.exe" --version
```

#### Opción 3: Usa Git Bash en lugar de PowerShell
```bash
# Git Bash tiene git integrado
git --version
```

---

### PowerShell ejecuta scripts bloqueados

**Problema**: No puedes ejecutar .bat o scripts

**Solución**:
```powershell
# Abre PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ahora puedes ejecutar scripts
.\ejecutar_app.bat
```

---

## 🔍 Diagnosticar Problemas

### Verificar instalación de Git
```powershell
git --version
```

Deberías ver: `git version 2.x.x.windows.x`

### Verificar configuración de Git
```powershell
git config --global user.name
git config --global user.email
```

Deberías ver tu nombre y email

### Verificar conexión con GitHub
```powershell
ssh -T git@github.com
```

Deberías ver: `Hi tu-usuario! You've successfully authenticated...`

### Verificar remoto configurado
```powershell
git remote -v
```

Deberías ver algo como:
```
origin  https://github.com/tu-usuario/automatizacion-tareas.git (fetch)
origin  https://github.com/tu-usuario/automatizacion-tareas.git (push)
```

---

## 🔐 Problemas de Seguridad

### Expuse mi token accidentalmente

**Acción inmediata**:
1. Ve a: https://github.com/settings/tokens
2. Encuentra el token expuesto
3. Haz clic en "Delete"
4. Genera un token nuevo

**GitHub lo detectará**: GitHub detecta tokens expuestos automáticamente

---

### Olvidé mi contraseña de GitHub

**Solución**:
1. Ve a: https://github.com/login
2. Click en "Forgot password?"
3. Sigue las instrucciones de recuperación
4. Recibe correo para resetear contraseña

---

## 💡 Tips para Evitar Problemas

1. **Siempre usa HTTPS** si no sabes SSH
2. **Guarda tu token en lugar seguro** (no en el código)
3. **Verifica la URL** antes de agregar origin
4. **Haz commits frecuentes** para no perder cambios
5. **Usa mensajes descriptivos** en commits

---

## 📱 Obtener Ayuda

Si el problema persiste:

1. **Lee la documentación**:
   - [GITHUB_VISUAL.md](GITHUB_VISUAL.md)
   - [GUIA_GITHUB.md](GUIA_GITHUB.md)

2. **Busca en Google**: "git error [tu-error]"

3. **GitHub Community**: https://github.community

4. **Stack Overflow**: https://stackoverflow.com/questions/tagged/git

---

## ✅ Checklist de Diagnóstico

- [ ] Git está instalado (`git --version`)
- [ ] Git está en PATH (funciona desde cualquier carpeta)
- [ ] Git está configurado (`git config --global user.name`)
- [ ] Tienes cuenta en GitHub
- [ ] Repositorio existe en GitHub
- [ ] Tienes token generado
- [ ] La URL es correcta
- [ ] La carpeta local tiene .git

---

## 🚀 Último Recurso

Si nada funciona, simplemente:

1. Elimina la carpeta `.git`:
```powershell
Remove-Item -Recurse .git -Force
```

2. Vuelve a empezar:
```powershell
git init
git add .
git commit -m "Respaldo inicial"
git remote add origin https://github.com/tu-usuario/automatizacion-tareas.git
git push -u origin main
```

---

**Recuerda**: Casi siempre el problema es la URL del repositorio o credenciales inválidas.
Verifica esos dos primero con: `git remote -v`
