# Script para iniciar el Sistema de Horarios con Redis
param(
    [switch]$StartRedis,
    [switch]$StartCelery,
    [switch]$StartDjango,
    [switch]$All
)

if ($All) {
    $StartRedis = $true
    $StartCelery = $true
    $StartDjango = $true
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "   Sistema de Gestión de Horarios" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Función para verificar si Redis está ejecutándose
function Test-RedisConnection {
    try {
        $result = & "C:\Program Files\Redis\redis-cli.exe" ping 2>$null
        return $result -eq "PONG"
    }
    catch {
        return $false
    }
}

# Función para iniciar Redis
function Start-RedisServer {
    Write-Host "[1/3] Iniciando Redis Server..." -ForegroundColor Yellow
    Start-Process -FilePath "C:\Program Files\Redis\redis-server.exe" -ArgumentList "--port", "6379" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    
    if (Test-RedisConnection) {
        Write-Host "✅ Redis iniciado correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al iniciar Redis" -ForegroundColor Red
        return $false
    }
    return $true
}

# Función para iniciar Celery
function Start-CeleryWorker {
    Write-Host "[2/3] Iniciando Celery Worker..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "manage.py", "celery", "worker", "--loglevel=info" -WindowStyle Normal
    Write-Host "✅ Celery Worker iniciado" -ForegroundColor Green
}

# Función para iniciar Django
function Start-DjangoServer {
    Write-Host "[3/3] Iniciando Django Server..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "manage.py", "runserver" -WindowStyle Normal
    Write-Host "✅ Django Server iniciado" -ForegroundColor Green
}

# Ejecutar según los parámetros
if ($StartRedis) {
    if (-not (Test-RedisConnection)) {
        if (-not (Start-RedisServer)) {
            Write-Host "Error: No se pudo iniciar Redis" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✅ Redis ya está ejecutándose" -ForegroundColor Green
    }
}

if ($StartCelery) {
    Start-CeleryWorker
}

if ($StartDjango) {
    Start-DjangoServer
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Sistema iniciado correctamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔴 Redis Server: localhost:6379" -ForegroundColor Cyan
Write-Host "🌐 Django Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "⚡ Celery Worker: Ejecutándose" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener todos los servicios" -ForegroundColor Yellow 