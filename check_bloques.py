#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.scheduling.models import BloquesHorariosDefinicion, DisponibilidadDocentes
from django.db.models import Count

def check_bloques_consistency():
    """Verificar la consistencia de los bloques horarios"""
    print("Verificando consistencia de bloques horarios...")
    
    # Verificar bloques con dia_semana nulo
    bloques_null = BloquesHorariosDefinicion.objects.filter(dia_semana__isnull=True)
    print(f"Bloques con dia_semana nulo: {bloques_null.count()}")
    
    # Verificar bloques duplicados por hora_inicio, hora_fin, turno
    from django.db.models import Count
    duplicates = BloquesHorariosDefinicion.objects.values(
        'hora_inicio', 'hora_fin', 'turno'
    ).annotate(
        count=Count('bloque_def_id')
    ).filter(count__gt=1)
    
    print(f"Grupos de bloques duplicados por hora/turno: {len(duplicates)}")
    
    # Mostrar algunos ejemplos de duplicados
    for dup in duplicates[:5]:
        bloques = BloquesHorariosDefinicion.objects.filter(
            hora_inicio=dup['hora_inicio'],
            hora_fin=dup['hora_fin'],
            turno=dup['turno']
        )
        print(f"  Duplicados para {dup['hora_inicio']}-{dup['hora_fin']} {dup['turno']}:")
        for b in bloques:
            print(f"    ID: {b.bloque_def_id}, dia_semana: {b.dia_semana}, nombre: {b.nombre_bloque}")
    
    # Verificar disponibilidades con inconsistencias
    print("\nVerificando inconsistencias en disponibilidades...")
    
    # Buscar disponibilidades donde el dia_semana no coincide con el del bloque
    inconsistencias = []
    for disp in DisponibilidadDocentes.objects.select_related('bloque_horario').all():
        if disp.bloque_horario.dia_semana is not None and disp.dia_semana != disp.bloque_horario.dia_semana:
            inconsistencias.append({
                'disponibilidad_id': disp.disponibilidad_id,
                'docente': disp.docente,
                'dia_semana_disp': disp.dia_semana,
                'dia_semana_bloque': disp.bloque_horario.dia_semana,
                'bloque_id': disp.bloque_horario.bloque_def_id,
                'hora_inicio': disp.bloque_horario.hora_inicio,
                'turno': disp.bloque_horario.turno
            })
    
    print(f"Inconsistencias encontradas: {len(inconsistencias)}")
    
    # Mostrar algunas inconsistencias
    for inc in inconsistencias[:10]:
        print(f"  Disponibilidad {inc['disponibilidad_id']}: "
              f"dia_semana={inc['dia_semana_disp']}, "
              f"bloque.dia_semana={inc['dia_semana_bloque']}, "
              f"bloque_id={inc['bloque_id']}, "
              f"hora={inc['hora_inicio']}, "
              f"turno={inc['turno']}")
    
    return inconsistencias

if __name__ == '__main__':
    check_bloques_consistency() 