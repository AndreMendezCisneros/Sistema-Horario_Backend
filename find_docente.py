#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_pontificia_horarios.settings')
django.setup()

from apps.users.models import Docentes

def find_docente():
    """Encontrar el docente correcto"""
    
    # Buscar docentes que contengan "Jeremias" o "Espino"
    docentes_jeremias = Docentes.objects.filter(nombres__icontains='Jeremias')
    docentes_espino = Docentes.objects.filter(apellidos__icontains='Espino')
    
    print("Docentes con nombre Jeremias:")
    for d in docentes_jeremias:
        print(f"  ID: {d.docente_id}, Nombre: {d.nombres} {d.apellidos}")
    
    print("\nDocentes con apellido Espino:")
    for d in docentes_espino:
        print(f"  ID: {d.docente_id}, Nombre: {d.nombres} {d.apellidos}")
    
    # Buscar por ID 17 (que aparece en los datos)
    docente_17 = Docentes.objects.filter(docente_id=17).first()
    if docente_17:
        print(f"\nDocente ID 17: {docente_17.nombres} {docente_17.apellidos}")

if __name__ == '__main__':
    find_docente() 