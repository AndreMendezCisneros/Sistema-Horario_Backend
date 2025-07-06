import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')

app = Celery('la_pontificia_horarios')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configuración de colas para load balancing
app.conf.update(
    # Colas específicas para diferentes tipos de tareas
    task_routes={
        # Tareas de generación de horarios (pesadas)
        'apps.scheduling.tasks.generar_horarios_task': {'queue': 'horarios'},
        'apps.scheduling.service.schedule_generator.*': {'queue': 'horarios'},
        
        # Tareas de métricas (rápidas)
        'apps.scheduling.events.update_dashboard_metrics': {'queue': 'metricas'},
        
        # Tareas de validación (rápidas)
        'apps.scheduling.service.conflict_validator.*': {'queue': 'validacion'},
        
        # Tareas de auditoría (baja prioridad)
        'apps.scheduling.events.log_conflict_for_audit': {'queue': 'auditoria'},
        'apps.scheduling.events.log_success_event': {'queue': 'auditoria'},
        'apps.scheduling.events.publish_horario_generated_event': {'queue': 'auditoria'},
        'apps.scheduling.events.publish_conflict_detected_event': {'queue': 'auditoria'},
    },
    
    # Configuración de colas
    task_default_queue='default',
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
        'horarios': {
            'exchange': 'horarios',
            'routing_key': 'horarios',
            'queue_arguments': {'x-max-priority': 10},
        },
        'metricas': {
            'exchange': 'metricas',
            'routing_key': 'metricas',
            'queue_arguments': {'x-max-priority': 5},
        },
        'validacion': {
            'exchange': 'validacion',
            'routing_key': 'validacion',
            'queue_arguments': {'x-max-priority': 7},
        },
        'auditoria': {
            'exchange': 'auditoria',
            'routing_key': 'auditoria',
            'queue_arguments': {'x-max-priority': 1},
        },
    },
    
    # Configuración de workers
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # Configuración de retry
    task_annotations={
        '*': {
            'rate_limit': '10/m',  # 10 tareas por minuto por defecto
        },
        'apps.scheduling.tasks.generar_horarios_task': {
            'rate_limit': '2/m',  # Solo 2 generaciones por minuto
            'time_limit': 1800,   # 30 minutos máximo
            'soft_time_limit': 1500,  # 25 minutos soft limit
        },
        'apps.scheduling.events.update_dashboard_metrics': {
            'rate_limit': '30/m',  # 30 actualizaciones por minuto
            'time_limit': 30,      # 30 segundos máximo
        },
    },

    # Configuración de Celery
    broker_url='redis://127.0.0.1:6379/0',
    result_backend='redis://127.0.0.1:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_max_tasks_per_child=1000,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 