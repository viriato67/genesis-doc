@echo off
title Compilando SIN HUMO...
echo.
echo  ====================================================
echo   Compilando SIN HUMO como ejecutable de Windows
echo  ====================================================
echo.

REM Verificar PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo  Instalando PyInstaller...
    pip install pyinstaller
)

REM Compilar
echo.
echo  Compilando... (puede tardar 1-2 minutos)
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "SinHumo" ^
    --add-data "sinhumo.ico;." ^
    savings_tracker.py

if %errorlevel% equ 0 (
    echo.
    echo  ====================================================
    echo   LISTO! El ejecutable esta en la carpeta "dist\"
    echo   Archivo: dist\SinHumo.exe
    echo  ====================================================
) else (
    echo.
    echo  Error durante la compilacion.
)

echo.
pause
