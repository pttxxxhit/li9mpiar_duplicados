@echo off
REM Script para subir el proyecto a GitHub
REM Uso: Edita los valores abajo y ejecuta este archivo

setlocal enabledelayedexpansion

REM ========== CONFIGURACION ==========
REM Cambia estos valores con tus datos

set GITHUB_USERNAME=tu-usuario-github
set REPO_NAME=automatizacion-tareas
set COMMIT_MESSAGE=Respaldo del proyecto: app Flet con duplicados y organización

REM ====================================

echo.
echo ===== SUBIR PROYECTO A GITHUB =====
echo.

REM Verificar que Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no está instalado
    echo Descargalo desde: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✓ Git detectado
echo.

REM Ir a la carpeta del proyecto
cd /d "%~dp0"
if not exist ".gitignore" (
    echo ERROR: No se encontró .gitignore
    echo Asegúrate de ejecutar esto en la carpeta correcta
    pause
    exit /b 1
)

echo ✓ Carpeta correcta detectada
echo.

REM Inicializar repositorio si no existe
if not exist ".git" (
    echo Inicializando repositorio local...
    git init
    echo ✓ Repositorio iniciado
) else (
    echo ✓ Repositorio ya existe
)
echo.

REM Agregar archivos
echo Agregando archivos...
git add .
echo ✓ Archivos agregados
echo.

REM Hacer commit
echo Creando commit...
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
    echo. No hay cambios que confirmar
) else (
    echo ✓ Commit creado
)
echo.

REM Configurar remoto
echo Verificando configuración de GitHub...
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo.
    echo IMPORTANTE: Necesitas configurar el remoto de GitHub
    echo.
    echo Ejecuta esto en PowerShell (reemplaza con tus datos):
    echo.
    echo git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
    echo git branch -M main
    echo git push -u origin main
    echo.
    echo O para SSH:
    echo git remote add origin git@github.com:%GITHUB_USERNAME%/%REPO_NAME%.git
    echo git branch -M main
    echo git push -u origin main
    echo.
) else (
    echo ✓ Remoto ya configurado
)
echo.

REM Intentar push
echo Subiendo a GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo subir a GitHub
    echo Posibles causas:
    echo 1. No tienes configurado el remoto (git remote add origin ...)
    echo 2. No tienes credenciales válidas
    echo 3. El repositorio no existe en GitHub
    echo.
    echo Consulta GUIA_GITHUB.md para instrucciones detalladas
    echo.
) else (
    echo ✓ Proyecto subido correctamente!
)
echo.

echo ===== PROCESO COMPLETADO =====
echo.
echo Verifica tu repositorio en:
echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.

pause
