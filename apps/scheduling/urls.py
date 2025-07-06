# apps/scheduling/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'grupos', views.GruposViewSet, basename='grupos')
router.register(r'bloques-horarios', views.BloquesHorariosDefinicionViewSet)
router.register(r'disponibilidad-docentes', views.DisponibilidadDocentesViewSet)
router.register(r'horarios-asignados', views.HorariosAsignadosViewSet)
router.register(r'configuracion-restricciones', views.ConfiguracionRestriccionesViewSet)
# Para la generación de horarios (no es un ModelViewSet estándar)
router.register(r'acciones-horario', views.GeneracionHorarioView, basename='acciones-horario')


urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints de métricas y auditoría
    path('metrics/', views.get_metrics, name='get_metrics'),
    path('metrics/<int:periodo_id>/', views.get_metrics, name='get_metrics_periodo'),
    path('audit/logs/', views.get_audit_logs, name='get_audit_logs'),
    path('audit/logs/<int:periodo_id>/', views.get_audit_logs, name='get_audit_logs_periodo'),
    path('audit/summary/', views.get_audit_summary, name='get_audit_summary'),
    path('audit/summary/<int:periodo_id>/', views.get_audit_summary, name='get_audit_summary_periodo'),
    path('health/', views.get_system_health, name='get_system_health'),
]
