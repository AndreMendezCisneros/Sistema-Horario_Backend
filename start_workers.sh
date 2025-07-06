#!/bin/bash

# Script para iniciar workers distribuidos de Celery
# Sistema de Horarios - Arquitectura Distribuida

echo "🚀 Iniciando Sistema Distribuido de Horarios..."
echo "================================================"

# Configuración
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER_PREFIX="horario_worker"

# Función para iniciar un worker
start_worker() {
    local queue_name=$1
    local worker_name=$2
    local concurrency=$3
    
    echo "📡 Iniciando worker: $worker_name (Cola: $queue_name, Concurrencia: $concurrency)"
    
    cd "$PROJECT_DIR"
    celery -A la_pontificia_horarios worker \
        --loglevel=info \
        --queues=$queue_name \
        --hostname=$worker_name@%h \
        --concurrency=$concurrency \
        --pidfile=/tmp/celery_${queue_name}.pid \
        --logfile=/tmp/celery_${queue_name}.log &
    
    echo "✅ Worker $worker_name iniciado (PID: $!)"
    echo "📝 Logs: /tmp/celery_${queue_name}.log"
    echo "---"
}

# Función para verificar si Redis está corriendo
check_redis() {
    echo "🔍 Verificando conexión a Redis..."
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis está corriendo"
        return 0
    else
        echo "❌ Redis no está corriendo. Iniciando Redis..."
        redis-server --daemonize yes
        sleep 2
        if redis-cli ping > /dev/null 2>&1; then
            echo "✅ Redis iniciado correctamente"
            return 0
        else
            echo "❌ Error iniciando Redis"
            return 1
        fi
    fi
}

# Función para mostrar estado de workers
show_status() {
    echo ""
    echo "📊 Estado de Workers:"
    echo "===================="
    
    for queue in horarios metricas validacion auditoria; do
        if [ -f "/tmp/celery_${queue}.pid" ]; then
            pid=$(cat "/tmp/celery_${queue}.pid")
            if ps -p $pid > /dev/null 2>&1; then
                echo "✅ $queue: Activo (PID: $pid)"
            else
                echo "❌ $queue: Inactivo"
            fi
        else
            echo "❌ $queue: No iniciado"
        fi
    done
}

# Función para detener todos los workers
stop_workers() {
    echo "🛑 Deteniendo todos los workers..."
    
    for queue in horarios metricas validacion auditoria; do
        if [ -f "/tmp/celery_${queue}.pid" ]; then
            pid=$(cat "/tmp/celery_${queue}.pid")
            if ps -p $pid > /dev/null 2>&1; then
                kill $pid
                echo "✅ Worker $queue detenido"
            fi
        fi
    done
    
    echo "✅ Todos los workers detenidos"
}

# Función para mostrar logs
show_logs() {
    local queue_name=$1
    if [ -f "/tmp/celery_${queue_name}.log" ]; then
        echo "📋 Logs de $queue_name:"
        echo "====================="
        tail -20 "/tmp/celery_${queue_name}.log"
    else
        echo "❌ No se encontraron logs para $queue_name"
    fi
}

# Menú principal
case "${1:-start}" in
    "start")
        # Verificar Redis
        if ! check_redis; then
            echo "❌ No se pudo conectar a Redis. Saliendo..."
            exit 1
        fi
        
        echo ""
        echo "🏗️  Iniciando Workers Distribuidos..."
        echo "====================================="
        
        # Worker para generación de horarios (tareas pesadas)
        start_worker "horarios" "${WORKER_PREFIX}_horarios" 2
        
        # Worker para métricas (tareas rápidas)
        start_worker "metricas" "${WORKER_PREFIX}_metricas" 4
        
        # Worker para validaciones (tareas rápidas)
        start_worker "validacion" "${WORKER_PREFIX}_validacion" 4
        
        # Worker para auditoría (tareas de baja prioridad)
        start_worker "auditoria" "${WORKER_PREFIX}_auditoria" 2
        
        echo ""
        echo "🎉 Sistema Distribuido iniciado correctamente!"
        echo ""
        echo "📊 Para monitorear: http://localhost:5555 (Flower)"
        echo "🛑 Para detener: ./start_workers.sh stop"
        echo "📋 Para ver logs: ./start_workers.sh logs <cola>"
        echo "📈 Para ver estado: ./start_workers.sh status"
        ;;
    
    "stop")
        stop_workers
        ;;
    
    "status")
        show_status
        ;;
    
    "logs")
        if [ -z "$2" ]; then
            echo "❌ Especifica una cola: ./start_workers.sh logs <cola>"
            echo "Colas disponibles: horarios, metricas, validacion, auditoria"
            exit 1
        fi
        show_logs "$2"
        ;;
    
    "restart")
        stop_workers
        sleep 2
        $0 start
        ;;
    
    *)
        echo "Uso: $0 {start|stop|status|logs|restart}"
        echo ""
        echo "Comandos:"
        echo "  start   - Iniciar todos los workers"
        echo "  stop    - Detener todos los workers"
        echo "  status  - Mostrar estado de workers"
        echo "  logs    - Mostrar logs de una cola específica"
        echo "  restart - Reiniciar todos los workers"
        echo ""
        echo "Ejemplo:"
        echo "  $0 start"
        echo "  $0 logs horarios"
        exit 1
        ;;
esac 