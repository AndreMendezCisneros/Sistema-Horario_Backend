from django.core.management.base import BaseCommand
from datetime import time, timedelta, date, datetime
from django.contrib.auth import get_user_model
from apps.academic_setup.models import (
    UnidadAcademica, Carrera, PeriodoAcademico, TiposEspacio, 
    EspaciosFisicos, Especialidades, Materias, Ciclo, Seccion, 
    MateriaEspecialidadesRequeridas
)
from apps.users.models import Docentes, DocenteEspecialidades
from apps.scheduling.models import Grupos, BloquesHorariosDefinicion, DisponibilidadDocentes
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos completos de La Pontificia.'

    def handle(self, *args, **options):
        User = get_user_model()
        fake = Faker('es_ES')
        
        self.stdout.write(self.style.SUCCESS('--- Poblando datos de La Pontificia ---'))

        # DATOS ACADÉMICOS COMPLETOS
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
                    "ADMINISTRACIÓN DE EMPRESAS": {
                        "codigo_base": "AE",
                        "plan_estudio_codigo": "20241",
                        "ciclos": [
                            [("EAE24-001", "Administración General", 48, 32), ("EAE24-002", "Matemática para los Negocios", 48, 32), ("EAE24-003", "Introducción a la Contabilidad", 48, 32), ("ETR24-001", "Intercomunicación Inicial", 48, 32), ("ETR24-002", "Ofimática Inicial", 48, 32)],
                            [("EAE24-004", "Fundamentos de Marketing", 48, 32), ("EAE24-005", "Matemática Financiera", 48, 32), ("EAE24-006", "Contabilidad General", 48, 32), ("ETR24-003", "Intercomunicación Avanzada", 48, 32), ("ETR24-004", "Ofimática Avanzada", 48, 32)],
                            [("EAE24-007", "Fundamentos de Finanzas", 48, 32), ("EAE24-008", "Investigación de Mercados", 48, 32), ("EAE24-009", "Derecho Empresarial", 48, 32), ("EAE24-010", "Estadística General", 48, 32), ("ETR24-005", "Psicología Organizacional", 32, 32), ("ETR24-010", "Introducción a la Ética", 32, 32)],
                            [("EAE24-011", "Elaboración de Procesos", 48, 32), ("EAE24-012", "Costos y Presupuestos", 48, 32), ("EAE24-013", "Análisis Cuantitativo para los Negocios", 48, 32), ("EAE24-014", "Estadística para los Negocios", 48, 32), ("ETR24-006", "Autorealización Personal", 32, 32), ("ETR24-011", "Ética Profesional", 32, 32)],
                            [("EAE24-015", "Derecho Laboral", 48, 32), ("EAE24-016", "Finanzas Empresariales", 48, 32), ("EAE24-017", "Administración de Operaciones", 48, 32), ("ETR24-007", "Atención al usuario", 48, 32), ("ETR24-012", "Didáctica del Razonamiento", 32, 32), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I", 0, 96)],
                            [("EAE24-018", "Talento Humano", 48, 32), ("EAE24-019", "Comportamiento Humano en las Organizaciones", 48, 32), ("EAE24-020", "Contabilidad Gerencial", 48, 32), ("ETR24-008", "Sistema de medición de la atención al usuario", 48, 32), ("ETR24-013", "Analisis de Situaciones Reales", 32, 32), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II", 0, 96)],
                            [("EAE24-021", "Administración Estratégica", 48, 32), ("EAE24-022", "Evaluación y Gestión de Proyectos", 48, 32), ("EAE24-023", "Cadena de suministro", 48, 32), ("ETR24-014", "Introducción a la Innovación", 32, 32), ("ETR24-019", "Desarrollo Emprendedor", 48, 32), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III", 0, 96)],
                            [("EAE24-024", "Estrategia Comercial", 48, 32), ("EAE24-025", "Micro y Pequeña Empresa", 48, 32), ("ETR24-009", "Plan de Negocios", 48, 32), ("ETR24-015", "Innovación en productos y servicios", 32, 32), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV", 0, 96)],
                            [("EAE24-026", "Marketing Estratégico", 48, 32), ("EAE24-027", "Administración Pública", 48, 32), ("EAE24-028", "E-business y Transformación Digital en las Empresas", 48, 32), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V", 0, 96)],
                            [("ETR24-016", "Fundamentos de Investigación Aplicada", 48, 32), ("ETR24-017", "Técnicas de Investigación Aplicada", 48, 32), ("ETR24-018", "Seminario de Tesis", 80, 32), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI", 0, 96)]
                        ]
                    },
                    "INGENIERIA DE SISTEMAS DE INFORMACIÓN": {
                        "codigo_base": "II",
                        "plan_estudio_codigo": "20241",
                        "ciclos": [
                            [("EIS24-001", "Arquitectura Web", 48, 32), ("EIS24-002", "Introducción a la Programación", 48, 32), ("EIS24-003", "Matemática Aplicada", 48, 32), ("ETR24-001", "Intercomunicación Inicial", 48, 32), ("ETR24-002", "Ofimática Inicial", 48, 32)],
                            [("EIS24-004", "Fundamentos de Algoritmia", 48, 32), ("EIS24-005", "Configuración de Aplicaciones", 48, 32), ("EIS24-006", "Introducción al Modelamiento de Procesos", 48, 32), ("ETR24-003", "Intercomunicación Avanzada", 48, 32), ("ETR24-004", "Ofimática Avanzada", 48, 32)],
                            [("EIS24-007", "Fundamentos de Estructura de Datos", 48, 32), ("EIS24-008", "Estadística Aplicada", 48, 32), ("EIS24-009", "Diseño de Sistemas en TI", 48, 32), ("EIS24-010", "Modelado de procesos en TI", 48, 32), ("ETR24-005", "Psicología Organizacional", 32, 32), ("ETR24-010", "Introducción a la Ética", 32, 32)],
                            [("EIS24-011", "Cyberseguridad", 48, 32), ("EIS24-012", "Gestión de Servicios en TI", 48, 32), ("EIS24-013", "Lenguaje de Programación", 48, 32), ("EIS24-014", "Programación orientada a Objetos", 48, 32), ("ETR24-006", "Autorealización Personal", 32, 32), ("ETR24-011", "Ética Profesional", 32, 32)],
                            [("EIS24-015", "Arquitectura de sistemas operativos", 48, 32), ("EIS24-016", "Programación de aplicaciones web", 48, 32), ("EIS24-017", "Sistemas Distribuidos", 48, 32), ("ETR24-007", "Atención al usuario", 48, 32), ("ETR24-012", "Didáctica del Razonamiento", 32, 32), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I", 0, 96)],
                            [("EIS24-018", "Soluciones móviles y cloud", 48, 32), ("EIS24-019", "Modelamiento y análisis de sistemas", 48, 32), ("EIS24-020", "Legislación en sistemas de información", 48, 32), ("ETR24-013", "Analisis de Situaciones Reales", 32, 32), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II", 0, 96)],
                            [("EIS24-021", "Arquitectura de software", 48, 32), ("EIS24-022", "Modelamiento de base de datos", 48, 32), ("EIS24-023", "Validación y pruebas de software", 48, 32), ("ETR24-008", "Sistema de medición de la atención al usuario", 48, 32), ("ETR24-014", "Introducción a la Innovación", 32, 32), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III", 0, 96)],
                            [("EIS24-024", "Auditoría de sistemas", 48, 32), ("EIS24-025", "Analítica con Big Data", 48, 32), ("EIS24-026", "Inteligencia artificial", 48, 32), ("ETR24-015", "Innovación en productos y servicios", 32, 32), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV", 0, 96)],
                            [("EIS24-027", "Bases de datos", 48, 32), ("EIS24-028", "Proyectos en TI", 48, 32), ("ETR24-009", "Plan de Negocios", 48, 32), ("ETR24-019", "Desarrollo Emprendedor", 48, 32), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V", 0, 96)],
                            [("ETR24-016", "Fundamentos de Investigación Aplicada", 48, 32), ("ETR24-017", "Técnicas de Investigación Aplicada", 48, 32), ("ETR24-018", "Seminario de Tesis", 80, 32), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI", 0, 96)]
                        ]
                    }
                }
            },
            "Instituto La Pontificia": {
                "tipo": "Instituto",
                "carreras": {
                    "ADMINISTRACIÓN DE EMPRESAS": {
                        "codigo_base": "AEI",
                        "plan_estudio_codigo": "2024",
                        "ciclos": [
                            [("AE23-001", "ADMINISTRACIÓN GENERAL", 5, 0), ("AE23-002", "INTERCOMUNICACIÓN INICIAL", 4, 0), ("AE23-003", "INTRODUCCIÓN A LA CONTABILIDAD", 4, 0), ("AE23-004", "FUNDAMENTOS DE MARKETING", 4, 0), ("AE23-005", "OFIMÁTICA INICIAL", 0, 4), ("AE23-006", "MATEMÁTICA PARA LOS NEGOCIOS I", 5, 0)],
                            [("AE23-007", "INTERCOMUNICACIÓN AVANZADA", 3, 0), ("AE23-008", "CONTABILIDAD FINANCIERA", 2, 2), ("AE23-009", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I", 0, 8), ("AE23-010", "OFIMÁTICA AVANZADA", 0, 4), ("AE23-011", "MARKETING ESTRATÉGICO", 5, 0), ("AE23-012", "MATEMÁTICA PARA LOS NEGOCIOS II", 6, 0)],
                            [("AE23-013", "ADMINISTRACIÓN ESTRATÉGICA I", 5, 0), ("AE23-014", "COMPORTAMIENTO HUMANO EN LAS ORGANIZACIONES", 4, 0), ("AE23-015", "AUTOREALIZACIÓN Y ÉTICA", 3, 0), ("AE23-016", "CONTABILIDAD DE COSTOS", 2, 2), ("AE23-017", "SERVICIO Y ATENCIÓN AL CLIENTE", 5, 0), ("AE23-018", "ESTADÍSTICA APLICADA", 3, 2)],
                            [("AE23-019", "ADMINISTRACIÓN DE OPERACIONES", 5, 0), ("AE23-020", "DERECHO EMPRESARIAL", 4, 0), ("AE23-021", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL", 3, 0), ("AE23-022", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II", 0, 8), ("AE23-023", "FUNDAMENTOS DE FINANZAS", 3, 2), ("AE23-024", "INDUCCIÓN AL MERCADO LABORAL", 3, 2)],
                            [("AE23-025", "DERECHO LABORAL Y TRIBUTARIO", 4, 0), ("AE23-026", "E-BUSINESS Y TRANSFORMACIÓN DIGITAL EN LAS EMPRESAS", 3, 2), ("AE23-027", "INVESTIGACIÓN DE MERCADOS", 3, 3), ("AE23-028", "GESTIÓN DEL TALENTO HUMANO", 4, 0), ("AE23-029", "MACRO Y MICRO ECONOMÍA", 4, 0), ("AE23-030", "LIDERAZGO Y TRABAJO EN EQUIPO", 3, 0)],
                            [("AE23-031", "ADMINISTRACIÓN PÚBLICA", 3, 2), ("AE23-032", "EVALUACIÓN Y GESTIÓN DE PROYECTOS", 3, 2), ("AE23-033", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III", 0, 8), ("AE23-034", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES", 3, 0), ("AE23-035", "PLAN DE NEGOCIOS", 4, 0), ("AE23-036", "ADQUISICIÓN DE BIENES Y SERVICIOS PÚBLICOS", 4, 0)]
                        ]
                    },
                    "CONTABILIDAD": {
                        "codigo_base": "CT",
                        "plan_estudio_codigo": "2024",
                        "ciclos": [
                            [("CT23-001", "ADMINISTRACIÓN GENERAL", 5, 0), ("CT23-002", "INTERCOMUNICACIÓN INICIAL", 4, 0), ("CT23-003", "FUNDAMENTOS DE MARKETING", 4, 0), ("CT23-004", "OFIMÁTICA INICIAL", 0, 4), ("CT23-005", "INTRODUCCIÓN A LA CONTABILIDAD", 4, 0), ("CT23-006", "MATEMÁTICA PARA LOS NEGOCIOS I", 6, 0)],
                            [("CT23-007", "INTERCOMUNICACIÓN AVANZADA", 3, 0), ("CT23-008", "CONTABILIDAD DE COSTOS", 3, 2), ("CT23-009", "CONTABILIDAD FINANCIERA I", 2, 2), ("CT23-010", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I", 0, 8), ("CT23-011", "OFIMÁTICA AVANZADA", 0, 4), ("CT23-012", "MATEMÁTICA PARA LOS NEGOCIOS II", 6, 0)],
                            [("CT23-013", "CONTABILIDAD FINANCIERA II", 4, 2), ("CT23-014", "DERECHO CIVIL Y COMERCIAL", 4, 0), ("CT23-015", "DERECHO TRIBUTARIO", 5, 0), ("CT23-016", "AUTOREALIZACIÓN Y ÉTICA", 3, 0), ("CT23-017", "FUNDAMENTOS DE FINANZAS", 2, 2), ("CT23-018", "MICROECONOMÍA PARA LOS NEGOCIOS", 3, 3)],
                            [("CT23-019", "ANÁLISIS Y REPORTES CONTABLES FINANCIEROS", 4, 0), ("CT23-020", "CONTABILIDAD FINANCIERA III", 4, 2), ("CT23-021", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL", 3, 0), ("CT23-022", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II", 0, 8), ("CT23-023", "FINANZAS CORPORATIVAS", 4, 2), ("CT23-024", "TRIBUTACIÓN APLICADA I", 4, 0)],
                            [("CT23-025", "AUDITORÍA FINANCIERA", 4, 2), ("CT23-026", "CONTABILIDAD GERENCIAL", 5, 0), ("CT23-027", "DERECHO LABORAL Y TRIBUTARIO", 4, 0), ("CT23-028", "AUDITORÍA Y CONTROL INTERNO", 4, 0), ("CT23-029", "LIDERAZGO Y TRABAJO EN EQUIPO", 3, 0), ("CT23-030", "TRIBUTACIÓN APLICADA II", 6, 0)],
                            [("CT23-031", "ADMINISTRACIÓN PÚBLICA", 3, 2), ("CT23-032", "AUDITORÍA TRIBUTARIA", 4, 0), ("CT23-033", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES", 3, 0), ("CT23-034", "CONTABILIDAD GUBERNAMENTAL", 2, 2), ("CT23-035", "EVALUACIÓN Y GESTIÓN DE PROYECTOS", 3, 2), ("CT23-036", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III", 0, 8)]
                        ]
                    },
                    "ENFERMERIA TÉCNICA": {
                        "codigo_base": "ET",
                        "plan_estudio_codigo": "2024",
                        "ciclos": [
                            [("ET23-001", "ANATOMÍA Y FISIOLOGÍA", 4, 2), ("ET23-002", "SALUD COMUNITARIA", 4, 2), ("ET23-003", "INTERCOMUNICACIÓN INICIAL", 4, 0), ("ET23-004", "OFIMÁTICA INICIAL", 0, 4), ("ET23-006", "PRIMEROS AUXILIOS", 3, 3)],
                            [("ET23-007", "BIOLOGÍA", 3, 2), ("ET23-008", "INTERCOMUNICACIÓN AVANZADA", 3, 0), ("ET23-009", "ENFERMERÍA BÁSICA I", 4, 3), ("ET23-010", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I", 0, 8), ("ET23-011", "TERMINOLOGÍA EN SALUD", 4, 0), ("ET23-012", "OFIMÁTICA AVANZADA", 0, 4)],
                            [("ET23-013", "ADMINISTRACIÓN DE MEDICAMENTOS", 3, 2), ("ET23-014", "AUTOREALIZACIÓN Y ÉTICA", 3, 0), ("ET23-015", "ENFERMERÍA BÁSICA II", 3, 3), ("ET23-016", "EPIDEMIOLOGÍA", 4, 0), ("ET23-017", "BIOSEGURIDAD", 3, 1), ("ET23-018", "FARMACOLOGÍA", 4, 0)],
                            [("ET23-019", "ASISTENCIA EN INMUNIZACIONES", 2, 2), ("ET23-020", "ASISTENCIA EN SALUD MATERNA Y DEL NEONATO", 1, 2), ("ET23-021", "ASISTENCIA QUIRURGICA", 3, 2), ("ET23-022", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL", 3, 0), ("ET23-023", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II", 0, 8), ("ET23-024", "SALUD PÚBLICA", 4, 0), ("ET23-037", "ASISTENCIA EN NEUMOLOGÍA", 3, 0)],
                            [("ET23-025", "ASISTENCIA EN FISIOTERAPIA Y REHABILITACIÓN", 3, 2), ("ET23-026", "ASISTENCIA EN MEDICINA ALTERNATIVA", 5, 0), ("ET23-027", "ASISTENCIA EN SALUD BUCAL", 4, 0), ("ET23-028", "LIDERAZGO Y TRABAJO EN EQUIPO", 3, 0), ("ET23-029", "SALUD DEL NIÑO Y DEL ADOLESCENTE", 3, 2), ("ET23-030", "SALUD OCUPACIONAL", 2, 2)],
                            [("ET23-031", "ASISTENCIA AL PACIENTE ONCOLOGICO Y CUIDADOS PALIATIVOS", 5, 0), ("ET23-032", "ASISTENCIA EN PROCEDIMIENTOS INVASIVOS Y NO INVASIVOS", 3, 2), ("ET23-033", "ASISTENCIA EN SALUD MENTAL Y PSIQUIATRIA", 5, 0), ("ET23-034", "ASISTENCIA GERIATRICA Y DEL ADULTO MAYOR", 3, 2), ("ET23-035", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III", 0, 8), ("ET23-036", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES", 3, 0)]
                        ]
                    }
                }
            }
        }

        # DATOS DE ESPACIOS
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

        # ESPECIALIDADES SUGERIDAS
        ESPECIALIDADES_SUGERIDAS = [
            "Contabilidad Financiera", "Tributación", "Finanzas Corporativas",
            "Administración Estratégica", "Marketing Digital", "Gestión del Talento Humano",
            "Desarrollo de Software", "Bases de Datos", "Ciberseguridad",
            "Redes y Comunicaciones", "Anatomía Humana", "Salud Pública",
            "Farmacología", "Didáctica y Pedagogía", "Ética Profesional",
            "Investigación Aplicada"
        ]

        NUM_DOCENTES = 80
        NUM_USUARIOS_ADMIN = 2
        DIAS_SEMANA = [1, 2, 3, 4, 5, 6]
        TURNOS_BLOQUES = {
            'M': [time(6, 0), time(7, 0), time(7, 0), time(8, 0), time(8, 0), time(9, 0), time(9, 0), time(10, 0), time(10, 0), time(11, 0), time(11, 0), time(12, 0), time(12, 0), time(13, 0)],
            'T': [time(13, 0), time(14, 0), time(14, 0), time(15, 0), time(15, 0), time(16, 0), time(16, 0), time(17, 0), time(17, 0), time(18, 0), time(18, 0), time(19, 0)],
            'N': [time(19, 0), time(20, 0), time(20, 0), time(21, 0), time(21, 0), time(22, 0)]
        }

        # 1. CREAR UNIDADES ACADÉMICAS
        self.stdout.write('Creando unidades académicas...')
        unidades = {}
        for nombre_unidad, datos in DATOS_ACADEMICOS.items():
            unidad, created = UnidadAcademica.objects.get_or_create(
                nombre_unidad=nombre_unidad,
                defaults={'descripcion': f"Unidad académica: {datos['tipo']}"}
            )
            if created:
                self.stdout.write(f'  ✓ Unidad creada: {nombre_unidad}')
            else:
                self.stdout.write(f'  ⚠ Unidad existente: {nombre_unidad}')
            unidades[nombre_unidad] = unidad

        # 2. CREAR ESPECIALIDADES
        self.stdout.write('Creando especialidades...')
        especialidades = {}
        for esp_nombre in ESPECIALIDADES_SUGERIDAS:
            especialidad, created = Especialidades.objects.get_or_create(
                nombre_especialidad=esp_nombre,
                defaults={'descripcion': f"Especialidad en {esp_nombre}"}
            )
            if created:
                self.stdout.write(f'  ✓ Especialidad creada: {esp_nombre}')
            else:
                self.stdout.write(f'  ⚠ Especialidad existente: {esp_nombre}')
            especialidades[esp_nombre] = especialidad

        # 3. CREAR TIPOS DE ESPACIO
        self.stdout.write('Creando tipos de espacio...')
        tipos_espacio = {}
        for tipo_nombre in DATOS_ESPACIOS.keys():
            tipo = TiposEspacio.objects.create(nombre_tipo_espacio=tipo_nombre)
            tipos_espacio[tipo_nombre] = tipo

        # 4. CREAR ESPACIOS FÍSICOS
        self.stdout.write('Creando espacios físicos...')
        espacios = []
        for tipo_nombre, edificios in DATOS_ESPACIOS.items():
            tipo = tipos_espacio[tipo_nombre]
            for edificio, config in edificios.items():
                for piso in range(1, config['pisos'] + 1):
                    for salon in range(1, config['salones_por_piso'] + 1):
                        nombre = f"{edificio}{piso:02d}{salon:02d}"
                        capacidad = 30 if tipo_nombre == "Aula Normal" else 25
                        espacio = EspaciosFisicos.objects.create(
                            nombre_espacio=nombre,
                            tipo_espacio=tipo,
                            capacidad=capacidad,
                            ubicacion=f"Edificio {edificio}, Piso {piso}",
                            unidad=unidades["Escuela Superior La Pontificia"]
                        )
                        espacios.append(espacio)

        # 5. CREAR PERÍODOS ACADÉMICOS
        self.stdout.write('Creando períodos académicos...')
        hoy = date.today()
        periodos = {}
        for i, nombre in enumerate(["2024-I", "2024-II", "2025-I"]):
            fecha_inicio = hoy + timedelta(days=i*120)
            fecha_fin = fecha_inicio + timedelta(days=119)
            activo = i == 0  # Solo el primero está activo
            periodo = PeriodoAcademico.objects.create(
                nombre_periodo=nombre,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                activo=activo
            )
            periodos[nombre] = periodo

        # 6. CREAR CARRERAS, CICLOS Y MATERIAS
        self.stdout.write('Creando carreras, ciclos y materias...')
        materias_creadas = {}
        
        for unidad_nombre, unidad_datos in DATOS_ACADEMICOS.items():
            unidad = unidades[unidad_nombre]
            
            for carrera_nombre, carrera_datos in unidad_datos['carreras'].items():
                # Crear carrera
                carrera = Carrera.objects.create(
                    nombre_carrera=carrera_nombre,
                    codigo_carrera=carrera_datos['codigo_base'],
                    unidad=unidad
                )
                
                # Crear ciclos y materias
                for i, ciclo_materias in enumerate(carrera_datos['ciclos'], 1):
                    ciclo = Ciclo.objects.create(
                        nombre_ciclo=f"Ciclo {i}",
                        orden=i,
                        carrera=carrera
                    )
                    
                    # Crear materias del ciclo
                    for codigo, nombre, horas_teo, horas_prac in ciclo_materias:
                        # Determinar tipo de espacio requerido
                        tipo_espacio = None
                        if "Cómputo" in nombre or "Programación" in nombre or "Software" in nombre:
                            tipo_espacio = tipos_espacio["Sala de Cómputo"]
                        elif "Laboratorio" in nombre or "Práctica" in nombre:
                            tipo_espacio = tipos_espacio["Aula Normal"]  # Por defecto
                        
                        materia, created = Materias.objects.get_or_create(
                            codigo_materia=codigo,
                            defaults={
                                'nombre_materia': nombre,
                                'descripcion': f"Materia del ciclo {i} de {carrera_nombre}",
                                'horas_academicas_teoricas': horas_teo,
                                'horas_academicas_practicas': horas_prac,
                                'horas_academicas_laboratorio': 0,
                                'requiere_tipo_espacio_especifico': tipo_espacio,
                                'estado': True
                            }
                        )
                        if created:
                            self.stdout.write(f'  ✓ Materia creada: {codigo} - {nombre}')
                        else:
                            self.stdout.write(f'  ⚠ Materia existente: {codigo} - {nombre}')
                        materias_creadas[codigo] = materia

        # 7. CREAR DOCENTES
        self.stdout.write('Creando docentes...')
        docentes = []
        for i in range(NUM_DOCENTES):
            user = User.objects.create_user(
                username=f"docente{i+1:03d}",
                password="test1234",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=f"docente{i+1:03d}@lapontificia.edu.pe"
            )
            
            docente = Docentes.objects.create(
                usuario=user,
                nombres=user.first_name,
                apellidos=user.last_name,
                codigo_docente=f"D{i+1:03d}",
                email=user.email,
                telefono=fake.phone_number(),
                tipo_contrato=random.choice(["Tiempo Completo", "Tiempo Parcial", "Por Horas"]),
                max_horas_semanales=random.choice([10, 15, 20, 25]),
                unidad_principal=unidades["Escuela Superior La Pontificia"]
            )
            docentes.append(docente)
            
            # Asignar especialidades aleatorias
            num_especialidades = random.randint(1, 3)
            especialidades_aleatorias = random.sample(ESPECIALIDADES_SUGERIDAS, num_especialidades)
            for esp_nombre in especialidades_aleatorias:
                DocenteEspecialidades.objects.create(
                    docente=docente,
                    especialidad=especialidades[esp_nombre]
                )

        # 8. CREAR BLOQUES HORARIOS (de 1 hora desde 6:00 hasta 22:00)
        self.stdout.write('Creando bloques horarios...')
        bloques = []
        hora_inicio = time(6, 0)
        hora_fin = time(22, 0)
        
        while hora_inicio < hora_fin:
            h_fin = time(hora_inicio.hour + 1, hora_inicio.minute)
            if h_fin > hora_fin:
                break
                
            # Determinar turno
            if hora_inicio < time(13, 0):
                turno = 'M'
            elif hora_inicio < time(19, 0):
                turno = 'T'
            else:
                turno = 'N'
            
            for dia in DIAS_SEMANA:
                nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'][dia-1]
                nombre_bloque = f"{nombre_dia} {hora_inicio.strftime('%H:%M')}-{h_fin.strftime('%H:%M')}"
                
                bloque = BloquesHorariosDefinicion.objects.create(
                    nombre_bloque=nombre_bloque,
                    hora_inicio=hora_inicio,
                    hora_fin=h_fin,
                    turno=turno,
                    dia_semana=dia
                )
                bloques.append(bloque)
            
            hora_inicio = h_fin

        # 9. CREAR DISPONIBILIDAD DE DOCENTES
        self.stdout.write('Creando disponibilidad de docentes...')
        periodo_activo = periodos["2024-I"]
        for docente in docentes:
            # Cada docente tiene disponibilidad en algunos bloques aleatorios
            bloques_aleatorios = random.sample(bloques, random.randint(10, 30))
            for bloque in bloques_aleatorios:
                DisponibilidadDocentes.objects.create(
                    docente=docente,
                    periodo=periodo_activo,
                    dia_semana=bloque.dia_semana,
                    bloque_horario=bloque,
                    esta_disponible=True
                )

        # 10. CREAR USUARIOS ADMINISTRADORES
        self.stdout.write('Creando usuarios administradores...')
        for i in range(NUM_USUARIOS_ADMIN):
            admin_user = User.objects.create_user(
                username=f"admin{i+1}",
                password="admin1234",
                first_name=f"Administrador",
                last_name=f"{i+1}",
                email=f"admin{i+1}@lapontificia.edu.pe",
                is_staff=True,
                is_superuser=True
            )

        self.stdout.write(self.style.SUCCESS('¡Datos de La Pontificia creados exitosamente!'))
        self.stdout.write(f'Se crearon:')
        self.stdout.write(f'- {len(unidades)} unidades académicas')
        self.stdout.write(f'- {len(especialidades)} especialidades')
        self.stdout.write(f'- {len(espacios)} espacios físicos')
        self.stdout.write(f'- {len(periodos)} períodos académicos')
        self.stdout.write(f'- {len(materias_creadas)} materias')
        self.stdout.write(f'- {len(docentes)} docentes')
        self.stdout.write(f'- {len(bloques)} bloques horarios')
        self.stdout.write(f'- {NUM_USUARIOS_ADMIN} usuarios administradores') 