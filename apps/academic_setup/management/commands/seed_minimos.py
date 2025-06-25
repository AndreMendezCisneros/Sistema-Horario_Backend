from django.core.management.base import BaseCommand
from datetime import time, timedelta, date, datetime
from django.contrib.auth import get_user_model
from apps.academic_setup.models import UnidadAcademica, Carrera, PeriodoAcademico, TiposEspacio, EspaciosFisicos, Especialidades, Materias, Ciclo, Seccion, MateriaEspecialidadesRequeridas
from apps.users.models import Docentes, DocenteEspecialidades
from apps.scheduling.models import Grupos, BloquesHorariosDefinicion, DisponibilidadDocentes

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos mínimos para pruebas de horarios.'

    def handle(self, *args, **options):
        User = get_user_model()
        self.stdout.write(self.style.SUCCESS('--- Poblando datos mínimos ---'))

        # 1. Unidades Académicas
        u1 = UnidadAcademica.objects.create(nombre_unidad="Unidad 1", descripcion="Unidad de prueba 1")
        u2 = UnidadAcademica.objects.create(nombre_unidad="Unidad 2", descripcion="Unidad de prueba 2")
        u3 = UnidadAcademica.objects.create(nombre_unidad="Unidad 3", descripcion="Unidad de prueba 3")

        # 2. Carreras
        c1 = Carrera.objects.create(nombre_carrera="Carrera 1", codigo_carrera="C1", unidad=u1)
        c2 = Carrera.objects.create(nombre_carrera="Carrera 2", codigo_carrera="C2", unidad=u2)
        c3 = Carrera.objects.create(nombre_carrera="Carrera 3", codigo_carrera="C3", unidad=u3)

        # 3. Periodos Académicos
        hoy = date.today()
        p1 = PeriodoAcademico.objects.create(nombre_periodo="2024-I", fecha_inicio=hoy, fecha_fin=hoy + timedelta(days=120), activo=True)
        p2 = PeriodoAcademico.objects.create(nombre_periodo="2024-II", fecha_inicio=hoy + timedelta(days=121), fecha_fin=hoy + timedelta(days=240), activo=False)
        p3 = PeriodoAcademico.objects.create(nombre_periodo="2025-I", fecha_inicio=hoy + timedelta(days=241), fecha_fin=hoy + timedelta(days=360), activo=False)

        # 4. Tipos de Espacio
        te1 = TiposEspacio.objects.create(nombre_tipo_espacio="Aula Común")
        te2 = TiposEspacio.objects.create(nombre_tipo_espacio="Laboratorio de Cómputo")
        te3 = TiposEspacio.objects.create(nombre_tipo_espacio="Laboratorio de Ciencias")

        # 5. Espacios Físicos (Aulas/Laboratorios)
        a1 = EspaciosFisicos.objects.create(nombre_espacio="Aula 101", tipo_espacio=te1, capacidad=30, ubicacion="Edificio A", unidad=u1)
        a2 = EspaciosFisicos.objects.create(nombre_espacio="Lab Comp 201", tipo_espacio=te2, capacidad=25, ubicacion="Edificio B", unidad=u2)
        a3 = EspaciosFisicos.objects.create(nombre_espacio="Lab Ciencias 301", tipo_espacio=te3, capacidad=20, ubicacion="Edificio C", unidad=u3)

        # 6. Especialidades
        esp1 = Especialidades.objects.create(nombre_especialidad="Especialidad 1", descripcion="Desc 1")
        esp2 = Especialidades.objects.create(nombre_especialidad="Especialidad 2", descripcion="Desc 2")
        esp3 = Especialidades.objects.create(nombre_especialidad="Especialidad 3", descripcion="Desc 3")

        # 7. Materias
        m1 = Materias.objects.create(
            codigo_materia="MAT001", nombre_materia="Materia 1", descripcion="Desc 1",
            horas_academicas_teoricas=2, horas_academicas_practicas=1, horas_academicas_laboratorio=1,
            requiere_tipo_espacio_especifico=te1, estado=True
        )
        m2 = Materias.objects.create(
            codigo_materia="MAT002", nombre_materia="Materia 2", descripcion="Desc 2",
            horas_academicas_teoricas=3, horas_academicas_practicas=2, horas_academicas_laboratorio=0,
            requiere_tipo_espacio_especifico=te2, estado=True
        )
        m3 = Materias.objects.create(
            codigo_materia="MAT003", nombre_materia="Materia 3", descripcion="Desc 3",
            horas_academicas_teoricas=1, horas_academicas_practicas=1, horas_academicas_laboratorio=2,
            requiere_tipo_espacio_especifico=te3, estado=True
        )

        # 8. Relacionar Materias y Especialidades
        MateriaEspecialidadesRequeridas.objects.create(materia=m1, especialidad=esp1)
        MateriaEspecialidadesRequeridas.objects.create(materia=m2, especialidad=esp2)
        MateriaEspecialidadesRequeridas.objects.create(materia=m3, especialidad=esp3)

        # 9. Ciclos
        ci1 = Ciclo.objects.create(nombre_ciclo="Ciclo 1", orden=1, carrera=c1)
        ci2 = Ciclo.objects.create(nombre_ciclo="Ciclo 2", orden=2, carrera=c2)
        ci3 = Ciclo.objects.create(nombre_ciclo="Ciclo 3", orden=3, carrera=c3)

        # 10. Secciones
        s1 = Seccion.objects.create(nombre_seccion="Sección A", ciclo=ci1, capacidad=30)
        s2 = Seccion.objects.create(nombre_seccion="Sección B", ciclo=ci2, capacidad=25)
        s3 = Seccion.objects.create(nombre_seccion="Sección C", ciclo=ci3, capacidad=20)

        # 11. Usuarios y Docentes
        user1 = User.objects.create_user(username="docente1", password="test1234", first_name="Docente", last_name="Uno")
        user2 = User.objects.create_user(username="docente2", password="test1234", first_name="Docente", last_name="Dos")
        user3 = User.objects.create_user(username="docente3", password="test1234", first_name="Docente", last_name="Tres")

        doc1 = Docentes.objects.create(
            usuario=user1,
            nombres="Docente",
            apellidos="Uno",
            codigo_docente="D001",
            email="docente1@ejemplo.com",
            telefono="111111",
            tipo_contrato="Tiempo Completo",
            max_horas_semanales=20,
            unidad_principal=u1
        )
        doc2 = Docentes.objects.create(
            usuario=user2,
            nombres="Docente",
            apellidos="Dos",
            codigo_docente="D002",
            email="docente2@ejemplo.com",
            telefono="222222",
            tipo_contrato="Tiempo Parcial",
            max_horas_semanales=15,
            unidad_principal=u2
        )
        doc3 = Docentes.objects.create(
            usuario=user3,
            nombres="Docente",
            apellidos="Tres",
            codigo_docente="D003",
            email="docente3@ejemplo.com",
            telefono="333333",
            tipo_contrato="Por Horas",
            max_horas_semanales=10,
            unidad_principal=u3
        )

        # 12. Relacionar Docentes y Especialidades
        DocenteEspecialidades.objects.create(docente=doc1, especialidad=esp1)
        DocenteEspecialidades.objects.create(docente=doc2, especialidad=esp2)
        DocenteEspecialidades.objects.create(docente=doc3, especialidad=esp3)

        # 13. Grupos
        g1 = Grupos.objects.create(codigo_grupo="G1", carrera=c1, periodo=p1, numero_estudiantes_estimado=20, turno_preferente="M", ciclo_semestral=1)
        g1.materias.add(m1)
        g2 = Grupos.objects.create(codigo_grupo="G2", carrera=c2, periodo=p1, numero_estudiantes_estimado=25, turno_preferente="T", ciclo_semestral=2)
        g2.materias.add(m2)
        g3 = Grupos.objects.create(codigo_grupo="G3", carrera=c3, periodo=p1, numero_estudiantes_estimado=15, turno_preferente="N", ciclo_semestral=3)
        g3.materias.add(m3)

        # 14. Bloques horarios (de 1 hora y 45 minutos, desde 7:00 a 22:00)
        hora_inicio = datetime.strptime("07:00", "%H:%M")
        hora_fin = datetime.strptime("22:00", "%H:%M")
        while hora_inicio < hora_fin:
            h_ini = hora_inicio.time()
            h_fin = (hora_inicio + timedelta(minutes=105)).time()  # 1h 45min = 105min
            if h_fin > hora_fin.time():
                break
            for dia in range(1, 6):  # Lunes a Viernes
                nombre = f"{['Lunes','Martes','Miércoles','Jueves','Viernes'][dia-1]} {h_ini.strftime('%H:%M')}-{h_fin.strftime('%H:%M')}"
                turno = "M" if h_ini < time(13,0) else ("T" if h_ini < time(19,0) else "N")
                BloquesHorariosDefinicion.objects.create(
                    nombre_bloque=nombre,
                    hora_inicio=h_ini,
                    hora_fin=h_fin,
                    turno=turno,
                    dia_semana=dia
                )
            hora_inicio += timedelta(minutes=105)

        # 15. Disponibilidad de docentes (todos los bloques del lunes para el primer periodo)
        bloques = BloquesHorariosDefinicion.objects.filter(dia_semana=1)
        for bloque in bloques:
            DisponibilidadDocentes.objects.create(docente=doc1, periodo=p1, dia_semana=1, bloque_horario=bloque, esta_disponible=True)
            DisponibilidadDocentes.objects.create(docente=doc2, periodo=p1, dia_semana=1, bloque_horario=bloque, esta_disponible=True)
            DisponibilidadDocentes.objects.create(docente=doc3, periodo=p1, dia_semana=1, bloque_horario=bloque, esta_disponible=True)

        self.stdout.write(self.style.SUCCESS('¡Datos mínimos creados exitosamente!'))