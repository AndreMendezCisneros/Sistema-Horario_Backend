# Script simple para iniciar el Sistema de Horarios
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Sistema de Gestión de Horarios" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar Redis
Write-Host "[1/3] Verificando Redis..." -ForegroundColor Yellow
try {
    $result = & "C:\Program Files\Redis\redis-cli.exe" ping 2>$null
    if ($result -eq "PONG") {
        Write-Host "✅ Redis ya está ejecutándose" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Redis no responde, iniciando..." -ForegroundColor Yellow
        Start-Process -FilePath "C:\Program Files\Redis\redis-server.exe" -ArgumentList "--port", "6379" -WindowStyle Minimized
        Start-Sleep -Seconds 3
        Write-Host "✅ Redis iniciado" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error con Redis" -ForegroundColor Red
}

# Iniciar Celery
Write-Host "[2/3] Iniciando Celery Worker..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "manage.py", "celery", "worker", "--loglevel=info" -WindowStyle Normal
Write-Host "✅ Celery Worker iniciado" -ForegroundColor Green

# Iniciar Django
Write-Host "[3/3] Iniciando Django Server..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "manage.py", "runserver" -WindowStyle Normal
Write-Host "✅ Django Server iniciado" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Sistema iniciado correctamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔴 Redis Server: localhost:6379" -ForegroundColor Cyan
Write-Host "🌐 Django Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "⚡ Celery Worker: Ejecutándose" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 