@echo off
echo ========================================
echo   Sistema de Gestion de Horarios
echo ========================================
echo.

echo [1/3] Verificando Redis...
"C:\Program Files\Redis\redis-cli.exe" ping >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Redis ya esta ejecutandose
) else (
    echo [INFO] Iniciando Redis...
    start "Redis Server" "C:\Program Files\Redis\redis-server.exe" --port 6379
    timeout /t 3 /nobreak >nul
    echo [OK] Redis iniciado
)

echo [2/3] Iniciando Celery Worker...
start "Celery Worker" cmd /k "python manage.py celery worker --loglevel=info"
echo [OK] Celery Worker iniciado

echo [3/3] Iniciando Django Server...
start "Django Server" cmd /k "python manage.py runserver"
echo [OK] Django Server iniciado

echo.
echo ========================================
echo   Sistema iniciado correctamente
echo ========================================
echo.
echo Redis Server: localhost:6379
echo Django Server: http://localhost:8000
echo Celery Worker: Ejecutandose
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul 