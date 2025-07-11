#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.scheduling.models import DisponibilidadDocentes
from apps.users.models import Docentes
from django.db import transaction

def clean_all_disponibilidad_docente():
    docente_id = 17  # Jeremias Espino Escriba
    docente = Docentes.objects.filter(docente_id=docente_id).first()
    if not docente:
        print(f"No se encontró el docente con ID {docente_id}")
        return
    print(f"Docente encontrado: {docente}")
    disponibilidades = DisponibilidadDocentes.objects.filter(docente=docente)
    total = disponibilidades.count()
    print(f"Disponibilidades encontradas: {total}")
    with transaction.atomic():
        disponibilidades.delete()
    print(f"Se eliminaron {total} registros de disponibilidad para el docente {docente}.")

if __name__ == '__main__':
    clean_all_disponibilidad_docente() 