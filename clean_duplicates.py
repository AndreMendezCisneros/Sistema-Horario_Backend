#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.scheduling.models import DisponibilidadDocentes
from django.db import transaction

def clean_duplicates():
    """Limpiar registros duplicados de disponibilidad de docentes"""
    print("Iniciando limpieza de duplicados...")
    
    # Obtener todos los registros agrupados por docente, periodo, dia_semana y bloque_horario
    from django.db.models import Count
    from django.db.models import Min
    
    # Encontrar duplicados
    duplicates = DisponibilidadDocentes.objects.values(
        'docente', 'periodo', 'dia_semana', 'bloque_horario'
    ).annotate(
        count=Count('disponibilidad_id')
    ).filter(count__gt=1)
    
    print(f"Encontrados {len(duplicates)} grupos de duplicados")
    
    cleaned_count = 0
    
    with transaction.atomic():
        for duplicate in duplicates:
            # Obtener todos los registros duplicados para este grupo
            records = DisponibilidadDocentes.objects.filter(
                docente_id=duplicate['docente'],
                periodo_id=duplicate['periodo'],
                dia_semana=duplicate['dia_semana'],
                bloque_horario_id=duplicate['bloque_horario']
            ).order_by('disponibilidad_id')
            
            # Mantener el primer registro (el más antiguo) y eliminar los demás
            first_record = records.first()
            records_to_delete = records.exclude(disponibilidad_id=first_record.disponibilidad_id)
            
            print(f"Eliminando {records_to_delete.count()} duplicados para docente {first_record.docente}, "
                  f"periodo {first_record.periodo}, día {first_record.dia_semana}, "
                  f"bloque {first_record.bloque_horario}")
            
            records_to_delete.delete()
            cleaned_count += records_to_delete.count()
    
    print(f"Limpieza completada. Se eliminaron {cleaned_count} registros duplicados.")
    
    # Verificar que no queden duplicados
    remaining_duplicates = DisponibilidadDocentes.objects.values(
        'docente', 'periodo', 'dia_semana', 'bloque_horario'
    ).annotate(
        count=Count('disponibilidad_id')
    ).filter(count__gt=1)
    
    if remaining_duplicates:
        print(f"ADVERTENCIA: Aún quedan {len(remaining_duplicates)} grupos de duplicados")
    else:
        print("Verificación completada: No quedan duplicados")

if __name__ == '__main__':
    clean_duplicates() 