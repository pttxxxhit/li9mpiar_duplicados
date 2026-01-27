# 📤 GITHUB BACKUP - PASOS VISUALES

## 🎯 OBJETIVO: Respaldo Privado en GitHub en 5 minutos

```
┌─────────────────────────────────────────────────────┐
│  PASO 1: Crear Repositorio en GitHub                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Abre: https://github.com/new                   │
│  2. Nombre: automatizacion-tareas                  │
│  3. Descripción: App para automatizar tareas       │
│  4. ⭕ Privado (IMPORTANTE)                        │
│  5. Crear repositorio                              │
│                                                     │
│  ✅ DONE: Repositorio creado en GitHub             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  PASO 2: Instalar Git (si no lo tienes)             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Descarga: https://git-scm.com/download/win    │
│  2. Ejecuta el instalador                          │
│  3. Sigue pasos por defecto                        │
│  4. Reinicia tu PC                                 │
│                                                     │
│  ✅ DONE: Git instalado                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  PASO 3: Configurar Git                             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Abre PowerShell y ejecuta:                        │
│                                                     │
│  git config --global user.name "Tu Nombre"        │
│  git config --global user.email "tu@email.com"    │
│                                                     │
│  Ejemplo:                                          │
│  git config --global user.name "Ernes"            │
│  git config --global user.email "ernes@gmail.com" │
│                                                     │
│  ✅ DONE: Git configurado                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  PASO 4: Crear Token en GitHub                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Ve a: https://github.com/settings/tokens      │
│  2. "Generate new token (classic)"                │
│  3. Nombre: "CLI Token"                           │
│  4. Expiration: 90 days                           │
│  5. Marca: repo (acceso completo)                 │
│  6. "Generate token"                              │
│  7. COPIA EL TOKEN (no lo verás de nuevo)        │
│                                                     │
│  ⚠️ GUARDA EN LUGAR SEGURO                        │
│                                                     │
│  ✅ DONE: Token generado                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  PASO 5: Subir Código a GitHub                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Abre PowerShell en la carpeta del proyecto:       │
│  C:\Users\ernes\Desktop\proyectofinal              │
│                                                     │
│  Ejecuta estos comandos:                          │
│                                                     │
│  git init                                         │
│  git add .                                        │
│  git commit -m "Respaldo: App Flet funcional"    │
│  git branch -M main                               │
│  git remote add origin \                          │
│    https://github.com/TU-USUARIO/\               │
│    automatizacion-tareas.git                      │
│  git push -u origin main                          │
│                                                     │
│  ⚠️ Cuando pida credenciales:                     │
│  Usuario: tu email de GitHub                      │
│  Contraseña: El TOKEN que copiaste en PASO 4     │
│                                                     │
│  ✅ DONE: Código en GitHub!                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  VERIFICAR: ¿Funcionó?                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Abre tu navegador                              │
│  2. Ve a: https://github.com/tu-usuario/\         │
│           automatizacion-tareas                    │
│  3. Verifica:                                      │
│     ✅ Ves todos tus archivos (app.py, etc)      │
│     ✅ El repo dice "Private" (🔒)                │
│     ✅ La rama es "main"                          │
│                                                     │
│  ✅ PERFECTO: ¡Respaldo completado!               │
└─────────────────────────────────────────────────────┘
```

## 🔄 FUTURO: Después de cambios

```powershell
cd C:\Users\ernes\Desktop\proyectofinal
git add .
git commit -m "Tu descripción aquí"
git push origin main
```

## 📋 CHECKLIST FINAL

- [ ] Cuente en GitHub creada
- [ ] Git instalado (`git --version`)
- [ ] Git configurado (name + email)
- [ ] Token de GitHub generado
- [ ] Repositorio creado en GitHub (PRIVADO)
- [ ] Código subido (`git push`)
- [ ] Verificado en GitHub (archivos visibles)
- [ ] Repositorio marcado como PRIVADO

## ❓ PROBLEMAS?

| Problema | Solución |
|----------|----------|
| "fatal: not a git repository" | `git init` en la carpeta correcta |
| "Authentication failed" | Usa el TOKEN como contraseña |
| "Repository not found" | Verifica que el repo exista |
| "Permission denied" | Crea token nuevo |

## 🎉 ¡HECHO!

Tu proyecto está respaldado de forma PRIVADA en GitHub.

**Puedes:**
- ✅ Ver el código desde cualquier lugar
- ✅ Descargar si necesitas cambiar de PC
- ✅ Compartir con colaboradores (opcional)
- ✅ Tener historial completo de cambios
- ✅ Recuperar versiones antiguas si necesitas

---

**Tiempo estimado**: 5-10 minutos
**Dificultad**: ⭐⭐ Fácil
**Resultado**: ✅ Código seguro en la nube
