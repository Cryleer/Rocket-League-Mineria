@echo off
chcp 65001 >nul
title Rocket Mineria - Inicio
color 0A

cls
echo ============================================================
echo        🚀 ROCKET MINERIA - INICIANDO SISTEMA
echo ============================================================
echo.

REM Iniciar API
echo [1/2] Iniciando API...
start "API - Puerto 8000" cmd /k "color 0B & cd /d "%~dp0" & python api\main.py"
timeout /t 3 >nul

REM Iniciar Dashboard
echo [2/2] Iniciando Dashboard...
start "Dashboard - Puerto 8050" cmd /k "color 0E & cd /d "%~dp0" & python dashboard\app.py"
timeout /t 3 >nul

cls
echo ============================================================
echo        ✅ SISTEMA INICIADO
echo ============================================================
echo.
echo   🌐 API:        http://localhost:8000/docs
echo   📊 Dashboard:  http://localhost:8050
echo.
echo ============================================================
echo.

REM Abrir navegadores
timeout /t 2 >nul
start http://localhost:8000/docs
timeout /t 1 >nul
start http://localhost:8050

echo ✅ Listo! Presiona cualquier tecla para cerrar esta ventana
pause >nul