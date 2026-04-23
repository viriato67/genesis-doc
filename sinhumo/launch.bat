@echo off
title SIN HUMO - Control de Ahorros

REM Buscar Python en el PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python no esta instalado o no esta en el PATH.
    echo.
    echo  Descarga Python desde: https://www.python.org/downloads/
    echo  Asegurate de marcar "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

REM Ejecutar la app
python "%~dp0savings_tracker.py"

if %errorlevel% neq 0 (
    echo.
    echo  Ocurrio un error al iniciar la aplicacion.
    pause
)
