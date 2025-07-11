#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.scheduling.models import DisponibilidadDocentes
from apps.users.models import Docentes
from django.db import transaction

def fix_sabado_issue():
    """Arreglar el problema específico con los bloques de Sábado"""
    
    # Usar el docente ID 17 (Jermi Espino Escriba)
    docente = Docentes.objects.filter(docente_id=17).first()
    if not docente:
        print("No se encontró el docente ID 17")
        return
    
    print(f"Docente encontrado: {docente}")
    
    # Buscar todas las disponibilidades de Sábado para este docente
    sabado_disponibilidades = DisponibilidadDocentes.objects.filter(
        docente=docente,
        dia_semana=6  # Sábado
    ).select_related('bloque_horario')
    
    print(f"Disponibilidades de Sábado encontradas: {sabado_disponibilidades.count()}")
    
    # Mostrar las disponibilidades actuales
    for disp in sabado_disponibilidades:
        print(f"ID: {disp.disponibilidad_id}, Bloque: {disp.bloque_horario.hora_inicio}, Disponible: {disp.esta_disponible}")
    
    # Eliminar todas las disponibilidades de Sábado
    with transaction.atomic():
        count = sabado_disponibilidades.count()
        sabado_disponibilidades.delete()
        print(f"Se eliminaron {count} disponibilidades de Sábado. Ahora puedes crear nuevas desde el frontend.")

if __name__ == '__main__':
    fix_sabado_issue() 