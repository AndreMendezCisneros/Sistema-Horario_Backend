# apps/scheduling/audit.py
from django.core.cache import cache
from django.utils import timezone
from apps.academic_setup.models import PeriodoAcademico
import json
import logging

logger = logging.getLogger(__name__)

class AuditManager:
    """Gestor de auditoría del sistema"""
    
    @staticmethod
    def log_success_event(periodo_id, resultado, user_id=None, task_id=None):
        """Registrar evento exitoso para auditoría"""
        try:
            # Obtener información del período
            periodo = PeriodoAcademico.objects.get(pk=periodo_id)
            
            # Crear registro de auditoría
            audit_record = {
                'evento': 'HORARIO_GENERADO_EXITOSAMENTE',
                'periodo_id': periodo_id,
                'periodo_nombre': periodo.nombre_periodo,
                'user_id': user_id,
                'task_id': task_id,
                'timestamp': timezone.now().isoformat(),
                'resultado': resultado,
                'estado': 'SUCCESS',
                'detalles': {
                    'total_horarios_generados': resultado.get('stats', {}).get('total_asignaciones', 0),
                    'conflictos_resueltos': resultado.get('stats', {}).get('conflictos_resueltos', 0),
                    'tiempo_procesamiento': resultado.get('stats', {}).get('tiempo_procesamiento', 0)
                }
            }
            
            # Guardar en cache con TTL de 24 horas
            cache_key = f'audit_success_{periodo_id}_{int(timezone.now().timestamp())}'
            cache.set(cache_key, json.dumps(audit_record), 86400)
            
            # Agregar a lista de eventos del período
            AuditManager.add_to_period_audit_list(periodo_id, audit_record)
            
            logger.info(f"Evento exitoso registrado para periodo {periodo_id}: {audit_record}")
            return {"status": "success", "audit_id": cache_key, "event_logged": True}
            
        except Exception as e:
            logger.error(f"Error registrando evento exitoso para periodo {periodo_id}: {e}")
            return {"status": "error", "error": str(e)}
    
    @staticmethod
    def log_conflict_event(conflicto_data, user_id=None, task_id=None):
        """Registrar conflicto para auditoría"""
        try:
            # Extraer información del conflicto
            periodo_id = conflicto_data.get('periodo_id')
            tipo_conflicto = conflicto_data.get('type', 'UNKNOWN')
            mensaje = conflicto_data.get('message', 'Sin mensaje')
            
            # Obtener información del período si está disponible
            periodo_nombre = "Desconocido"
            if periodo_id:
                try:
                    periodo = PeriodoAcademico.objects.get(pk=periodo_id)
                    periodo_nombre = periodo.nombre_periodo
                except:
                    pass
            
            # Crear registro de auditoría
            audit_record = {
                'evento': 'CONFLICTO_DETECTADO',
                'periodo_id': periodo_id,
                'periodo_nombre': periodo_nombre,
                'user_id': user_id,
                'task_id': task_id,
                'timestamp': timezone.now().isoformat(),
                'tipo_conflicto': tipo_conflicto,
                'mensaje': mensaje,
                'estado': 'WARNING',
                'detalles': conflicto_data
            }
            
            # Guardar en cache con TTL de 24 horas
            cache_key = f'audit_conflict_{periodo_id or "global"}_{int(timezone.now().timestamp())}'
            cache.set(cache_key, json.dumps(audit_record), 86400)
            
            # Agregar a lista de eventos del período
            if periodo_id:
                AuditManager.add_to_period_audit_list(periodo_id, audit_record)
            
            # Agregar a lista global de conflictos
            AuditManager.add_to_global_conflicts_list(audit_record)
            
            logger.warning(f"Conflicto registrado para auditoría: {audit_record}")
            return {"status": "success", "audit_id": cache_key, "conflict_logged": True}
            
        except Exception as e:
            logger.error(f"Error registrando conflicto para auditoría: {e}")
            return {"status": "error", "error": str(e)}
    
    @staticmethod
    def add_to_period_audit_list(periodo_id, audit_record):
        """Agregar evento a la lista de auditoría del período"""
        try:
            # Obtener lista existente
            audit_list = cache.get(f'audit_list_periodo_{periodo_id}', [])
            
            # Agregar nuevo evento
            audit_list.append(audit_record)
            
            # Mantener solo los últimos 100 eventos
            if len(audit_list) > 100:
                audit_list = audit_list[-100:]
            
            # Guardar lista actualizada
            cache.set(f'audit_list_periodo_{periodo_id}', audit_list, 86400)
            
        except Exception as e:
            logger.error(f"Error agregando evento a lista de auditoría: {e}")
    
    @staticmethod
    def add_to_global_conflicts_list(audit_record):
        """Agregar conflicto a la lista global de conflictos"""
        try:
            # Obtener lista existente
            conflicts_list = cache.get('global_conflicts_list', [])
            
            # Agregar nuevo conflicto
            conflicts_list.append(audit_record)
            
            # Mantener solo los últimos 50 conflictos
            if len(conflicts_list) > 50:
                conflicts_list = conflicts_list[-50:]
            
            # Guardar lista actualizada
            cache.set('global_conflicts_list', conflicts_list, 86400)
            
        except Exception as e:
            logger.error(f"Error agregando conflicto a lista global: {e}")
    
    @staticmethod
    def get_audit_logs(periodo_id=None, limit=50):
        """Obtener logs de auditoría"""
        try:
            if periodo_id:
                # Logs específicos del período
                audit_list = cache.get(f'audit_list_periodo_{periodo_id}', [])
                return audit_list[-limit:] if audit_list else []
            else:
                # Logs globales de conflictos
                conflicts_list = cache.get('global_conflicts_list', [])
                return conflicts_list[-limit:] if conflicts_list else []
                
        except Exception as e:
            logger.error(f"Error obteniendo logs de auditoría: {e}")
            return []
    
    @staticmethod
    def get_audit_summary(periodo_id=None):
        """Obtener resumen de auditoría"""
        try:
            if periodo_id:
                # Resumen del período
                audit_list = cache.get(f'audit_list_periodo_{periodo_id}', [])
                
                total_events = len(audit_list)
                success_events = len([e for e in audit_list if e.get('estado') == 'SUCCESS'])
                conflict_events = len([e for e in audit_list if e.get('estado') == 'WARNING'])
                
                return {
                    'periodo_id': periodo_id,
                    'total_eventos': total_events,
                    'eventos_exitosos': success_events,
                    'eventos_conflicto': conflict_events,
                    'tasa_exito': round((success_events / total_events * 100), 2) if total_events > 0 else 0
                }
            else:
                # Resumen global
                conflicts_list = cache.get('global_conflicts_list', [])
                
                return {
                    'total_conflictos': len(conflicts_list),
                    'ultimos_conflictos': conflicts_list[-10:] if conflicts_list else []
                }
                
        except Exception as e:
            logger.error(f"Error obteniendo resumen de auditoría: {e}")
            return {"error": str(e)} 