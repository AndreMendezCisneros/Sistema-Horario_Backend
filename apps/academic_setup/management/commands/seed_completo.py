from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from datetime import time, datetime, date
import random

from apps.academic_setup.models import (
    TipoUnidadAcademica, UnidadAcademica, Carrera, Ciclo, PeriodoAcademico,
    TiposEspacio, EspaciosFisicos, Materias, CarreraMaterias, Especialidades
)
from apps.users.models import Docentes
from apps.scheduling.models import (
    Grupos, BloquesHorariosDefinicion, DisponibilidadDocentes, ConfiguracionRestricciones
)

# === DATOS REALES PARA POBLAR ===
DATOS_ACADEMICOS = {
    "Escuela Superior La Pontificia": {
        "tipo": "Escuela Profesional",
        "carreras": {
            "CONTABILIDAD Y FINANZAS": {
                "codigo_base": "CF",
                "plan_estudio_codigo": "20241",
                "ciclos": [
                    [("ECF24-001", "Introducción a la Contabilidad", 48, 32), ("ECF24-002", "Matemática para los Negocios", 48, 32), ("ECF24-003", "Introducción al Sistema Tributario", 48, 32), ("ETR24-001", "Intercomunicación Inicial", 48, 32), ("ETR24-002", "Ofimática Inicial", 48, 32)],
                    [("ECF24-004", "Registros y Operaciones Contables", 48, 32), ("ECF24-005", "Matemática Financiera", 48, 32), ("ECF24-006", "Fundamentos de Finanzas", 48, 32), ("ETR24-003", "Intercomunicación Avanzada", 48, 32), ("ETR24-004", "Ofimática Avanzada", 48, 32)],
                    [("ECF24-007", "Contabilidad de Sociedades", 48, 32), ("ECF24-008", "Sistema Tributario", 48, 32), ("ECF24-009", "Regitro de Planillas", 48, 32), ("ECF24-010", "Finanzas Empresariales", 48, 32), ("ETR24-005", "Psicología Organizacional", 32, 32), ("ETR24-010", "Introducción a la Ética", 32, 32)],
                    [("ECF24-011", "Contabilidad de Costos", 48, 32), ("ECF24-012", "Derecho Tributario", 48, 32), ("ECF24-013", "Derecho Comercial", 48, 32), ("ECF24-014", "Declaraciones Juradas Mensuales", 48, 32), ("ETR24-006", "Autorealización Personal", 32, 32), ("ETR24-011", "Ética Profesional", 32, 32)],
                    [("ECF24-015", "Análisis de Reportes Contables", 48, 32), ("ECF24-016", "Contabilidad de MYPES", 48, 32), ("ECF24-017", "Contabilidad Financiera", 48, 32), ("ETR24-007", "Atención al usuario", 48, 32), ("ETR24-012", "Didáctica del Razonamiento", 32, 32), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I", 0, 96)],
                    [("ECF24-018", "Evaluación financiera de proyectos", 48, 32), ("ECF24-019", "Análisis de Reportes Financieros", 48, 32), ("ECF24-020", "Elaboración de Estados Financieros", 48, 32), ("ECF24-021", "Introducción a la Contabilidad Pública", 48, 32), ("ETR24-013", "Analisis de Situaciones Reales", 32, 32), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II", 0, 96)],
                    [("ECF24-022", "Aplicación de las Normas Internacionales de Contabilidad", 48, 32), ("ECF24-023", "Contabilidad Pública", 48, 32), ("ECF24-024", "Auditoría y Control Interno", 48, 32), ("ETR24-008", "Sistema de medición de la atención al usuario", 48, 32), ("ETR24-014", "Introducción a la Innovación", 32, 32), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III", 0, 96)],
                    [("ECF24-025", "Análisis de Riesgos", 48, 32), ("ECF24-026", "Valorización de Empresas", 32, 32), ("ECF24-027", "Auditoría Tributaria", 32, 32), ("ETR24-015", "Innovación en productos y servicios", 32, 32), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV", 0, 96)],
                    [("ECF24-028", "Portafolio de Inversiones", 16, 32), ("ECF24-029", "Planificación Financiera", 16, 32), ("ECF24-030", "Contabilidad Gerencial", 16, 32), ("ETR24-009", "Plan de Negocios", 48, 32), ("ETR24-019", "Desarrollo Emprendedor", 48, 32), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V", 0, 96)],
                    [("ETR24-016", "Fundamentos de Investigación Aplicada", 48, 32), ("ETR24-017", "Técnicas de Investigación Aplicada", 48, 32), ("ETR24-018", "Seminario de Tesis", 80, 32), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI", 0, 96)]
                ]
            },
            # ... (agrega aquí las demás carreras y ciclos de tu estructura)
        }
    },
    # ... (agrega aquí el resto de unidades académicas e institutos)
}

DATOS_ESPACIOS = {
    "Aula Normal": {
        "A": {"pisos": 5, "salones_por_piso": 10},
        "B": {"pisos": 5, "salones_por_piso": 5},
    },
    "Sala de Cómputo": {
        "C": {"pisos": 4, "salones_por_piso": 1},
        "D": {"pisos": 4, "salones_por_piso": 2},
    }
}

ESPECIALIDADES_SUGERIDAS = [
    "Contabilidad Financiera", "Tributación", "Finanzas Corporativas", "Administración Estratégica", "Marketing Digital", "Gestión del Talento Humano", "Desarrollo de Software", "Bases de Datos", "Ciberseguridad", "Redes y Comunicaciones", "Anatomía Humana", "Salud Pública", "Farmacología", "Didáctica y Pedagogía", "Ética Profesional", "Investigación Aplicada"
]

NUM_DOCENTES = 80
NUM_USUARIOS_ADMIN = 2
DIAS_SEMANA = [1, 2, 3, 4, 5, 6]
TURNOS_BLOQUES = [
    (time(6, 0), time(7, 0)),
    (time(7, 0), time(8, 0)),
    (time(8, 0), time(9, 0)),
    (time(9, 0), time(10, 0)),
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)),
    (time(13, 0), time(14, 0)),
    (time(14, 0), time(15, 0)),
    (time(15, 0), time(16, 0)),
    (time(16, 0), time(17, 0)),
    (time(17, 0), time(18, 0)),
    (time(18, 0), time(19, 0)),
    (time(19, 0), time(20, 0)),
    (time(20, 0), time(21, 0)),
    (time(21, 0), time(22, 0)),
]

class Command(BaseCommand):
    help = 'Siembra la base de datos con todos los datos necesarios para el sistema de horarios.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("=== Iniciando siembra completa de datos ===")
        self._limpiar_datos_previos()
        self._crear_especialidades()
        unidades = self._crear_unidades_academicas()
        tipos_espacio = self._crear_tipos_espacio()
        espacios_fisicos = self._crear_espacios_fisicos(tipos_espacio, unidades)
        periodo = self._crear_periodo_academico()
        bloques_horarios = self._crear_bloques_horarios()
        self._procesar_planes_de_estudio(unidades)
        self._crear_docentes_y_admins(unidades)
        self.stdout.write(self.style.SUCCESS("=== Siembra completa finalizada exitosamente ==="))

    def _limpiar_datos_previos(self):
        self.stdout.write("Limpiando datos existentes...")
        # NO limpiar HorariosAsignados como solicitaste
        DisponibilidadDocentes.objects.all().delete()
        ConfiguracionRestricciones.objects.all().delete()
        Grupos.objects.all().delete()
        CarreraMaterias.objects.all().delete()
        Materias.objects.all().delete()
        Ciclo.objects.all().delete()
        Carrera.objects.all().delete()
        EspaciosFisicos.objects.all().delete()
        TiposEspacio.objects.all().delete()
        Docentes.objects.all().delete()
        UnidadAcademica.objects.all().delete()
        TipoUnidadAcademica.objects.all().delete()
        PeriodoAcademico.objects.all().delete()
        BloquesHorariosDefinicion.objects.all().delete()
        Especialidades.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Datos previos eliminados."))

    def _crear_especialidades(self):
        for nombre in ESPECIALIDADES_SUGERIDAS:
            Especialidades.objects.get_or_create(nombre_especialidad=nombre)

    def _crear_unidades_academicas(self):
        unidades = {}
        for nombre, datos in DATOS_ACADEMICOS.items():
            tipo, _ = TipoUnidadAcademica.objects.get_or_create(nombre_tipo=datos["tipo"])
            unidad, _ = UnidadAcademica.objects.get_or_create(nombre_unidad=nombre, defaults={"tipo_unidad": tipo})
            unidades[nombre] = unidad
        return unidades

    def _crear_tipos_espacio(self):
        tipos = {}
        for tipo_nombre in DATOS_ESPACIOS.keys():
            tipo, _ = TiposEspacio.objects.get_or_create(nombre_tipo_espacio=tipo_nombre)
            tipos[tipo_nombre] = tipo
        return tipos

    def _crear_espacios_fisicos(self, tipos_espacio, unidades):
        for tipo_nombre, edificios in DATOS_ESPACIOS.items():
            for edificio, info in edificios.items():
                for piso in range(1, info["pisos"] + 1):
                    for num in range(1, info["salones_por_piso"] + 1):
                        nombre = f"{tipo_nombre} {edificio}-{piso:02d}{num:02d}"
                        EspaciosFisicos.objects.get_or_create(
                            nombre_espacio=nombre,
                            tipo_espacio=tipos_espacio[tipo_nombre],
                            capacidad=40,
                            unidad=list(unidades.values())[0]  # Puedes mejorar la asignación
                        )

    def _crear_periodo_academico(self):
        periodo, _ = PeriodoAcademico.objects.get_or_create(
            nombre_periodo="2024-II",
            defaults={
                'fecha_inicio': date(2024, 8, 1),
                'fecha_fin': date(2024, 12, 15),
                'activo': True
            }
        )
        return periodo

    def _crear_bloques_horarios(self):
        bloques = []
        for dia in DIAS_SEMANA:
            for hora_inicio, hora_fin in TURNOS_BLOQUES:
                # Determinar turno
                if hora_inicio < time(12, 0):
                    turno = 'M'
                elif hora_inicio < time(18, 0):
                    turno = 'T'
                else:
                    turno = 'N'
                nombre = f"{turno}-{dia} {hora_inicio.strftime('%H:%M')}-{hora_fin.strftime('%H:%M')}"
                bloque, _ = BloquesHorariosDefinicion.objects.get_or_create(
                    nombre_bloque=nombre,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    turno=turno,
                    dia_semana=dia
                )
                bloques.append(bloque)
        return bloques

    def _procesar_planes_de_estudio(self, unidades):
        for unidad_nombre, datos_unidad in DATOS_ACADEMICOS.items():
            unidad = unidades[unidad_nombre]
            for carrera_nombre, datos_carrera in datos_unidad["carreras"].items():
                carrera, _ = Carrera.objects.get_or_create(
                    nombre_carrera=carrera_nombre,
                    codigo_carrera=datos_carrera["codigo_base"],
                    unidad=unidad
                )
                for idx_ciclo, materias_ciclo in enumerate(datos_carrera["ciclos"], start=1):
                    ciclo, _ = Ciclo.objects.get_or_create(
                        nombre_ciclo=f"Ciclo {idx_ciclo}",
                        orden=idx_ciclo,
                        carrera=carrera
                    )
                    for cod, nombre, horas_teo, horas_pra in materias_ciclo:
                        materia, _ = Materias.objects.get_or_create(
                            codigo_materia=cod,
                            nombre_materia=nombre,
                            horas_academicas_teoricas=horas_teo,
                            horas_academicas_practicas=horas_pra
                        )
                        CarreraMaterias.objects.get_or_create(
                            carrera=carrera,
                            materia=materia,
                            ciclo=ciclo
                        )

    def _crear_docentes_y_admins(self, unidades):
        # Crear usuarios admin
        for i in range(1, NUM_USUARIOS_ADMIN+1):
            username = f"admin{i}"
            user, _ = User.objects.get_or_create(username=username, defaults={"is_superuser": True, "is_staff": True})
            user.set_password("admin1234")
            user.save()
        # Crear docentes
        especialidades = list(Especialidades.objects.all())
        for i in range(1, NUM_DOCENTES+1):
            username = f"docente{i}"
            user, _ = User.objects.get_or_create(username=username)
            user.set_password("docente1234")
            user.save()
            Docentes.objects.get_or_create(
                usuario=user,
                nombres=f"Docente{i}",
                apellidos="Prueba",
                codigo_docente=f"D{i:03d}",
                email=f"docente{i}@ejemplo.com",
                telefono=f"99999{i:03d}",
                tipo_contrato="Tiempo Completo",
                max_horas_semanales=20,
                unidad_principal=list(unidades.values())[0]
            )

    def _crear_disponibilidad_docentes(self, docentes, periodo, bloques_horarios):
        self.stdout.write("Creando Disponibilidad de Docentes...")
        disponibilidades_creadas = 0
        
        for docente in docentes:
            for bloque in bloques_horarios:
                # 80% de probabilidad de estar disponible
                if random.random() < 0.8:
                    disponibilidad, created = DisponibilidadDocentes.objects.get_or_create(
                        docente=docente,
                        periodo=periodo,
                        dia_semana=bloque.dia_semana,
                        bloque_horario=bloque,
                        defaults={
                            'esta_disponible': True,
                            'preferencia': random.choice([0, 0, 0, 1, -1]),  # Más neutral
                            'origen_carga': 'MANUAL'
                        }
                    )
                    if created:
                        disponibilidades_creadas += 1
        
        self.stdout.write(f"    Creadas {disponibilidades_creadas} disponibilidades de docentes")

    def _crear_configuraciones_restricciones(self, periodo):
        self.stdout.write("Creando Configuraciones de Restricciones...")
        
        restricciones_data = [
            {
                'codigo': 'MAX_HORAS_DIA_DOCENTE',
                'descripcion': 'Ningún docente puede exceder las 6 horas de clase al día',
                'tipo': 'GLOBAL',
                'valor': '6'
            },
            {
                'codigo': 'MAX_HORAS_SEMANA_DOCENTE',
                'descripcion': 'Ningún docente puede exceder las 20 horas de clase por semana',
                'tipo': 'GLOBAL',
                'valor': '20'
            },
            {
                'codigo': 'NO_CLASES_SABADO',
                'descripcion': 'No se pueden programar clases los sábados',
                'tipo': 'GLOBAL',
                'valor': '6'  # Código del sábado
            },
            {
                'codigo': 'NO_CLASES_DOMINGO',
                'descripcion': 'No se pueden programar clases los domingos',
                'tipo': 'GLOBAL',
                'valor': '7'  # Código del domingo
            },
            {
                'codigo': 'CAPACIDAD_AULA',
                'descripcion': 'El número de estudiantes no puede exceder la capacidad del aula',
                'tipo': 'AULA',
                'valor': '100%'
            },
            {
                'codigo': 'LABORATORIO_SOLO_PRACTICAS',
                'descripcion': 'Los laboratorios solo pueden usarse para clases prácticas',
                'tipo': 'AULA',
                'valor': 'SOLO_PRACTICAS'
            }
        ]
        
        for restriccion_data in restricciones_data:
            ConfiguracionRestricciones.objects.get_or_create(
                codigo_restriccion=restriccion_data['codigo'],
                defaults={
                    'descripcion': restriccion_data['descripcion'],
                    'tipo_aplicacion': restriccion_data['tipo'],
                    'valor_parametro': restriccion_data['valor'],
                    'periodo_aplicable': periodo,
                    'esta_activa': True
                }
            )
        
        self.stdout.write(f"    Creadas {len(restricciones_data)} configuraciones de restricciones") 