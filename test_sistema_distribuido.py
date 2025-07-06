#!/usr/bin/env python
"""
Script de prueba para el Sistema Distribuido de Horarios
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.scheduling.metrics import MetricsManager
from apps.scheduling.audit import AuditManager
from apps.scheduling.circuit_breaker import CircuitBreaker
from apps.academic_setup.models import PeriodoAcademico

def test_metrics():
    """Probar sistema de métricas"""
    print("🧪 PROBANDO SISTEMA DE MÉTRICAS...")
    
    try:
        # Obtener métricas globales
        global_metrics = MetricsManager.get_metrics()
        print(f"✅ Métricas globales obtenidas: {global_metrics}")
        
        # Probar con un período específico (si existe)
        periodos = PeriodoAcademico.objects.all()[:1]
        if periodos:
            periodo = periodos[0]
            periodo_metrics = MetricsManager.update_schedule_generation_metrics(periodo.periodo_id)
            print(f"✅ Métricas del período {periodo.periodo_id}: {periodo_metrics}")
        
        return True
    except Exception as e:
        print(f"❌ Error en métricas: {e}")
        return False

def test_audit():
    """Probar sistema de auditoría"""
    print("\n🧪 PROBANDO SISTEMA DE AUDITORÍA...")
    
    try:
        # Probar registro de evento exitoso
        test_result = {
            'stats': {
                'total_asignaciones': 10,
                'conflictos_resueltos': 2,
                'tiempo_procesamiento': 30.5
            }
        }
        
        audit_result = AuditManager.log_success_event(1, test_result, user_id=1, task_id="test_task_123")
        print(f"✅ Evento exitoso registrado: {audit_result}")
        
        # Probar registro de conflicto
        conflict_data = {
            'periodo_id': 1,
            'type': 'docente_conflict',
            'message': 'Docente ya asignado en este bloque'
        }
        
        conflict_result = AuditManager.log_conflict_event(conflict_data, user_id=1, task_id="test_task_456")
        print(f"✅ Conflicto registrado: {conflict_result}")
        
        # Obtener logs de auditoría
        audit_logs = AuditManager.get_audit_logs(limit=10)
        print(f"✅ Logs de auditoría obtenidos: {len(audit_logs)} registros")
        
        # Obtener resumen de auditoría
        audit_summary = AuditManager.get_audit_summary()
        print(f"✅ Resumen de auditoría: {audit_summary}")
        
        return True
    except Exception as e:
        print(f"❌ Error en auditoría: {e}")
        return False

def test_circuit_breaker():
    """Probar circuit breaker"""
    print("\n🧪 PROBANDO CIRCUIT BREAKER...")
    
    try:
        # Crear instancia de circuit breaker
        cb = CircuitBreaker('test_service', failure_threshold=2, recovery_timeout=10)
        
        # Función de prueba que falla
        def failing_function():
            raise Exception("Error simulado")
        
        # Función de prueba que funciona
        def working_function():
            return "Éxito"
        
        # Probar función que funciona
        result = cb.call(working_function)
        print(f"✅ Circuit breaker con función exitosa: {result}")
        
        # Probar función que falla
        try:
            cb.call(failing_function)
        except Exception as e:
            print(f"✅ Circuit breaker detectó fallo: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error en circuit breaker: {e}")
        return False

def test_integration():
    """Probar integración completa"""
    print("\n🧪 PROBANDO INTEGRACIÓN COMPLETA...")
    
    try:
        # Simular generación de horarios
        periodo_id = 1
        resultado_simulado = {
            'stats': {
                'total_asignaciones': 25,
                'conflictos_resueltos': 5,
                'tiempo_procesamiento': 120.5
            },
            'status': 'COMPLETED'
        }
        
        # Actualizar métricas
        metrics = MetricsManager.update_schedule_generation_metrics(periodo_id)
        print(f"✅ Métricas actualizadas: {metrics}")
        
        # Registrar en auditoría
        audit_result = AuditManager.log_success_event(periodo_id, resultado_simulado)
        print(f"✅ Auditoría registrada: {audit_result}")
        
        # Incrementar contador de conflictos
        MetricsManager.increment_conflict_counter(periodo_id)
        print("✅ Contador de conflictos incrementado")
        
        # Obtener estado final
        final_metrics = MetricsManager.get_metrics(periodo_id)
        final_audit = AuditManager.get_audit_summary(periodo_id)
        
        print(f"✅ Estado final - Métricas: {final_metrics}")
        print(f"✅ Estado final - Auditoría: {final_audit}")
        
        return True
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DISTRIBUIDO")
    print("=" * 50)
    
    tests = [
        ("Métricas", test_metrics),
        ("Auditoría", test_audit),
        ("Circuit Breaker", test_circuit_breaker),
        ("Integración", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Mostrar resultados
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE LAS PRUEBAS")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n🎯 RESUMEN: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema distribuido está funcionando correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main() 