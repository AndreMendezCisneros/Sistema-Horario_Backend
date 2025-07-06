# apps/scheduling/circuit_breaker.py
import time
import logging
from functools import wraps
from django.core.cache import cache

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Circuit Breaker simple para tolerancia a fallos"""
    
    def __init__(self, name, failure_threshold=5, recovery_timeout=60, expected_exception=Exception):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        # Estados del circuit breaker
        self.STATE_CLOSED = 'CLOSED'
        self.STATE_OPEN = 'OPEN'
        self.STATE_HALF_OPEN = 'HALF_OPEN'
    
    def _get_cache_key(self, suffix):
        return f"circuit_breaker:{self.name}:{suffix}"
    
    def _get_state(self):
        """Obtener estado actual del circuit breaker"""
        return cache.get(self._get_cache_key('state'), self.STATE_CLOSED)
    
    def _set_state(self, state):
        """Establecer estado del circuit breaker"""
        cache.set(self._get_cache_key('state'), state, self.recovery_timeout)
    
    def _get_failure_count(self):
        """Obtener contador de fallos"""
        return cache.get(self._get_cache_key('failures'), 0)
    
    def _increment_failure_count(self):
        """Incrementar contador de fallos"""
        failures = self._get_failure_count() + 1
        cache.set(self._get_cache_key('failures'), failures, self.recovery_timeout)
        return failures
    
    def _reset_failure_count(self):
        """Resetear contador de fallos"""
        cache.delete(self._get_cache_key('failures'))
    
    def _get_last_failure_time(self):
        """Obtener tiempo del último fallo"""
        return cache.get(self._get_cache_key('last_failure'), 0)
    
    def _set_last_failure_time(self):
        """Establecer tiempo del último fallo"""
        cache.set(self._get_cache_key('last_failure'), time.time(), self.recovery_timeout)
    
    def call(self, func, *args, **kwargs):
        """Ejecutar función con circuit breaker"""
        state = self._get_state()
        
        if state == self.STATE_OPEN:
            # Circuito abierto - verificar si es tiempo de recuperación
            last_failure = self._get_last_failure_time()
            if time.time() - last_failure > self.recovery_timeout:
                logger.info(f"Circuit Breaker {self.name}: Cambiando a HALF_OPEN")
                self._set_state(self.STATE_HALF_OPEN)
                state = self.STATE_HALF_OPEN
            else:
                raise Exception(f"Circuit Breaker {self.name} está ABIERTO")
        
        try:
            # Intentar ejecutar la función
            result = func(*args, **kwargs)
            
            # Éxito - resetear fallos si estaba en HALF_OPEN
            if state == self.STATE_HALF_OPEN:
                logger.info(f"Circuit Breaker {self.name}: Recuperación exitosa, cerrando circuito")
                self._set_state(self.STATE_CLOSED)
                self._reset_failure_count()
            
            return result
            
        except self.expected_exception as e:
            # Fallo - incrementar contador
            failures = self._increment_failure_count()
            self._set_last_failure_time()
            
            logger.warning(f"Circuit Breaker {self.name}: Fallo #{failures}")
            
            # Si alcanzamos el umbral, abrir el circuito
            if failures >= self.failure_threshold:
                logger.error(f"Circuit Breaker {self.name}: Abriendo circuito después de {failures} fallos")
                self._set_state(self.STATE_OPEN)
            
            raise e

def circuit_breaker(name, failure_threshold=5, recovery_timeout=60, expected_exception=Exception):
    """Decorador para circuit breaker"""
    def decorator(func):
        cb = CircuitBreaker(name, failure_threshold, recovery_timeout, expected_exception)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        
        return wrapper
    return decorator

# Ejemplo de uso con tareas de Celery
@circuit_breaker('database_operations', failure_threshold=3, recovery_timeout=30)
def safe_database_operation(operation_func, *args, **kwargs):
    """Operación de base de datos con circuit breaker"""
    return operation_func(*args, **kwargs)

@circuit_breaker('email_service', failure_threshold=5, recovery_timeout=60)
def safe_email_send(email_func, *args, **kwargs):
    """Envío de emails con circuit breaker"""
    return email_func(*args, **kwargs)

@circuit_breaker('external_api', failure_threshold=3, recovery_timeout=120)
def safe_external_api_call(api_func, *args, **kwargs):
    """Llamadas a APIs externas con circuit breaker"""
    return api_func(*args, **kwargs) 