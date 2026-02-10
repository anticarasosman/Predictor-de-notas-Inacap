@echo off
REM Script para iniciar la aplicacion con tunel SSH (Red Corporativa)
REM Haz doble clic en este archivo para ejecutar

cls
echo.
echo ========================================
echo   HERRAMIENTA INACAP - RED CORPORATIVA
echo ========================================
echo.

REM Ejecutar el script PowerShell con bypass de politica
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar-con-tunel.ps1"
