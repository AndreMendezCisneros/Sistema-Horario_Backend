# apps/scheduling/events.py
from celery import shared_task
from .metrics import MetricsManager
from .audit import AuditManager
import logging

logger = logging.getLogger(__name__)

# Eventos del sistema de horarios
class HorarioEvents:
    HORARIO_GENERADO = "horario.generado"
    CONFLICTO_DETECTADO = "conflicto.detectado"

@shared_task
def publish_horario_generated_event(periodo_id, resultado):
    """Evento: Horario generado exitosamente"""
    logger.info(f"Evento: Horario generado para periodo {periodo_id}")
    
    # Procesar el evento
    update_dashboard_metrics.delay(periodo_id)
    log_success_event.delay(periodo_id, resultado)
    
    return {"status": "success", "event": HorarioEvents.HORARIO_GENERADO}

@shared_task
def publish_conflict_detected_event(conflicto_data):
    """Evento: Conflicto detectado en horarios"""
    logger.warning(f"Evento: Conflicto detectado - {conflicto_data}")
    
    # Procesar el conflicto
    log_conflict_for_audit.delay(conflicto_data)
    
    return {"status": "warning", "event": HorarioEvents.CONFLICTO_DETECTADO}

@shared_task
def update_dashboard_metrics(periodo_id):
    """Actualizar métricas del dashboard"""
    logger.info(f"Actualizando métricas para periodo {periodo_id}")
    
    # Usar el MetricsManager real
    metrics = MetricsManager.update_schedule_generation_metrics(periodo_id)
    
    return {"status": "success", "metrics_updated": True, "periodo_id": periodo_id, "metrics": metrics}

@shared_task
def log_success_event(periodo_id, resultado):
    """Registrar evento exitoso para auditoría"""
    logger.info(f"Evento exitoso registrado para periodo {periodo_id}: {resultado}")
    
    # Usar el AuditManager real
    audit_result = AuditManager.log_success_event(periodo_id, resultado)
    
    return {"status": "success", "event_logged": True, "audit_result": audit_result}

@shared_task
def log_conflict_for_audit(conflicto_data):
    """Registrar conflicto para auditoría"""
    logger.warning(f"Conflicto registrado para auditoría: {conflicto_data}")
    
    # Usar el AuditManager real
    audit_result = AuditManager.log_conflict_event(conflicto_data)
    
    # Incrementar contador de conflictos en métricas
    periodo_id = conflicto_data.get('periodo_id')
    if periodo_id:
        MetricsManager.increment_conflict_counter(periodo_id)
    
    return {"status": "success", "conflict_logged": True, "audit_result": audit_result} 