from django.core.cache import cache
from django.db.models import Count, Q
from apps.scheduling.models import HorariosAsignados
from apps.academic_setup.models import PeriodoAcademico
from apps.users.models import Docentes
import json
import logging

logger = logging.getLogger(__name__)

class MetricsManager:
    """Gestor de métricas en tiempo real"""
    
    @staticmethod
    def update_schedule_generation_metrics(periodo_id):
        """Actualizar métricas de generación de horarios"""
        try:
            # Obtener datos del período
            periodo = PeriodoAcademico.objects.get(pk=periodo_id)
            
            # Contar horarios generados
            total_horarios = HorariosAsignados.objects.filter(periodo=periodo).count()
            
            # Contar docentes con horarios asignados
            docentes_con_horarios = Docentes.objects.filter(
                clases_asignadas__periodo=periodo
            ).distinct().count()
            
            # Contar total de docentes activos
            total_docentes = Docentes.objects.filter(usuario__is_active=True).count()
            
            # Calcular porcentaje de cobertura
            cobertura_docentes = (docentes_con_horarios / total_docentes * 100) if total_docentes > 0 else 0
            
            # Contar conflictos detectados
            conflictos = cache.get(f'conflictos_periodo_{periodo_id}', 0)
            
            # Calcular tasa de éxito
            tasa_exito = 100 - (conflictos / total_horarios * 100) if total_horarios > 0 else 100
            
            # Crear métricas
            metrics = {
                'periodo_id': periodo_id,
                'periodo_nombre': periodo.nombre_periodo,
                'total_horarios': total_horarios,
                'docentes_con_horarios': docentes_con_horarios,
                'total_docentes': total_docentes,
                'cobertura_docentes': round(cobertura_docentes, 2),
                'conflictos_detectados': conflictos,
                'tasa_exito': round(tasa_exito, 2),
                'ultima_actualizacion': periodo.fecha_actualizacion.isoformat() if periodo.fecha_actualizacion else None
            }
            
            # Guardar en cache con TTL de 1 hora
            cache.set(f'metrics_periodo_{periodo_id}', json.dumps(metrics), 3600)
            
            # Actualizar métricas globales
            MetricsManager.update_global_metrics()
            
            logger.info(f"Métricas actualizadas para periodo {periodo_id}: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error actualizando métricas para periodo {periodo_id}: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def update_global_metrics():
        """Actualizar métricas globales del sistema"""
        try:
            # Total de períodos activos
            periodos_activos = PeriodoAcademico.objects.filter(activo=True).count()
            
            # Total de horarios en el sistema
            total_horarios_sistema = HorariosAsignados.objects.count()
            
            # Total de docentes activos
            total_docentes_sistema = Docentes.objects.filter(usuario__is_active=True).count()
            
            # Total de conflictos en el sistema
            total_conflictos = cache.get('total_conflictos_sistema', 0)
            
            global_metrics = {
                'periodos_activos': periodos_activos,
                'total_horarios_sistema': total_horarios_sistema,
                'total_docentes_sistema': total_docentes_sistema,
                'total_conflictos_sistema': total_conflictos,
                'ultima_actualizacion': 'now'
            }
            
            cache.set('global_metrics', json.dumps(global_metrics), 3600)
            logger.info(f"Métricas globales actualizadas: {global_metrics}")
            
        except Exception as e:
            logger.error(f"Error actualizando métricas globales: {e}")
    
    @staticmethod
    def increment_conflict_counter(periodo_id):
        """Incrementar contador de conflictos"""
        try:
            # Incrementar conflictos del período
            conflictos_periodo = cache.get(f'conflictos_periodo_{periodo_id}', 0)
            cache.set(f'conflictos_periodo_{periodo_id}', conflictos_periodo + 1, 3600)
            
            # Incrementar conflictos globales
            total_conflictos = cache.get('total_conflictos_sistema', 0)
            cache.set('total_conflictos_sistema', total_conflictos + 1, 3600)
            
            logger.info(f"Contador de conflictos incrementado para periodo {periodo_id}")
            
        except Exception as e:
            logger.error(f"Error incrementando contador de conflictos: {e}")
    
    @staticmethod
    def get_metrics(periodo_id=None):
        """Obtener métricas"""
        try:
            if periodo_id:
                # Métricas específicas del período
                metrics_data = cache.get(f'metrics_periodo_{periodo_id}')
                if metrics_data:
                    return json.loads(metrics_data)
                else:
                    # Si no existen, calcularlas
                    return MetricsManager.update_schedule_generation_metrics(periodo_id)
            else:
                # Métricas globales
                global_metrics = cache.get('global_metrics')
                if global_metrics:
                    return json.loads(global_metrics)
                else:
                    # Si no existen, calcularlas
                    MetricsManager.update_global_metrics()
                    return json.loads(cache.get('global_metrics', '{}'))
                    
        except Exception as e:
            logger.error(f"Error obteniendo métricas: {e}")
            return {"error": str(e)} 