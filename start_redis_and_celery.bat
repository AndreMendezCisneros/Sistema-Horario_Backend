@echo off
echo ========================================
echo   Iniciando Sistema de Horarios
echo ========================================
echo.

echo [1/3] Iniciando Redis Server...
start "Redis Server" "C:\Program Files\Redis\redis-server.exe" --port 6379
timeout /t 3 /nobreak > nul

echo [2/3] Verificando conexion a Redis...
"C:\Program Files\Redis\redis-cli.exe" ping
if %errorlevel% neq 0 (
    echo ERROR: Redis no responde
    pause
    exit /b 1
)

echo [3/3] Iniciando Celery Worker...
start "Celery Worker" cmd /k "python manage.py celery worker --loglevel=info"

echo.
echo ========================================
echo   Sistema iniciado correctamente
echo ========================================
echo.
echo Redis Server: http://localhost:6379
echo Django Server: http://localhost:8000
echo.
echo Presiona cualquier tecla para cerrar...
pause > nul 