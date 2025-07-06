from django.core.management.base import BaseCommand
from apps.academic_setup.models import Materias, Carrera, Ciclo, PeriodoAcademico
from apps.scheduling.models import Grupos

class Command(BaseCommand):
    help = 'Asigna las materias a sus carreras y ciclos correspondientes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Asignando materias a carreras ---'))
        
        # Obtener el período activo
        try:
            periodo_activo = PeriodoAcademico.objects.get(activo=True)
            self.stdout.write(f'Usando período activo: {periodo_activo.nombre_periodo}')
        except PeriodoAcademico.DoesNotExist:
            self.stdout.write('❌ No hay período activo. Creando uno...')
            from datetime import date, timedelta
            hoy = date.today()
            periodo_activo = PeriodoAcademico.objects.create(
                nombre_periodo="2024-I",
                fecha_inicio=hoy,
                fecha_fin=hoy + timedelta(days=120),
                activo=True
            )
            self.stdout.write(f'✓ Período creado: {periodo_activo.nombre_periodo}')

        # DATOS ACADÉMICOS CON LA ESTRUCTURA CORRECTA
        DATOS_ACADEMICOS = {
            "Escuela Superior La Pontificia": {
                "carreras": {
                    "CONTABILIDAD Y FINANZAS": {
                        "codigo_base": "CF",
                        "ciclos": [
                            [("ECF24-001", "Introducción a la Contabilidad"), ("ECF24-002", "Matemática para los Negocios"), ("ECF24-003", "Introducción al Sistema Tributario"), ("ETR24-001", "Intercomunicación Inicial"), ("ETR24-002", "Ofimática Inicial")],
                            [("ECF24-004", "Registros y Operaciones Contables"), ("ECF24-005", "Matemática Financiera"), ("ECF24-006", "Fundamentos de Finanzas"), ("ETR24-003", "Intercomunicación Avanzada"), ("ETR24-004", "Ofimática Avanzada")],
                            [("ECF24-007", "Contabilidad de Sociedades"), ("ECF24-008", "Sistema Tributario"), ("ECF24-009", "Regitro de Planillas"), ("ECF24-010", "Finanzas Empresariales"), ("ETR24-005", "Psicología Organizacional"), ("ETR24-010", "Introducción a la Ética")],
                            [("ECF24-011", "Contabilidad de Costos"), ("ECF24-012", "Derecho Tributario"), ("ECF24-013", "Derecho Comercial"), ("ECF24-014", "Declaraciones Juradas Mensuales"), ("ETR24-006", "Autorealización Personal"), ("ETR24-011", "Ética Profesional")],
                            [("ECF24-015", "Análisis de Reportes Contables"), ("ECF24-016", "Contabilidad de MYPES"), ("ECF24-017", "Contabilidad Financiera"), ("ETR24-007", "Atención al usuario"), ("ETR24-012", "Didáctica del Razonamiento"), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I")],
                            [("ECF24-018", "Evaluación financiera de proyectos"), ("ECF24-019", "Análisis de Reportes Financieros"), ("ECF24-020", "Elaboración de Estados Financieros"), ("ECF24-021", "Introducción a la Contabilidad Pública"), ("ETR24-013", "Analisis de Situaciones Reales"), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II")],
                            [("ECF24-022", "Aplicación de las Normas Internacionales de Contabilidad"), ("ECF24-023", "Contabilidad Pública"), ("ECF24-024", "Auditoría y Control Interno"), ("ETR24-008", "Sistema de medición de la atención al usuario"), ("ETR24-014", "Introducción a la Innovación"), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III")],
                            [("ECF24-025", "Análisis de Riesgos"), ("ECF24-026", "Valorización de Empresas"), ("ECF24-027", "Auditoría Tributaria"), ("ETR24-015", "Innovación en productos y servicios"), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV")],
                            [("ECF24-028", "Portafolio de Inversiones"), ("ECF24-029", "Planificación Financiera"), ("ECF24-030", "Contabilidad Gerencial"), ("ETR24-009", "Plan de Negocios"), ("ETR24-019", "Desarrollo Emprendedor"), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V")],
                            [("ETR24-016", "Fundamentos de Investigación Aplicada"), ("ETR24-017", "Técnicas de Investigación Aplicada"), ("ETR24-018", "Seminario de Tesis"), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI")]
                        ]
                    },
                    "ADMINISTRACIÓN DE EMPRESAS": {
                        "codigo_base": "AE",
                        "ciclos": [
                            [("EAE24-001", "Administración General"), ("EAE24-002", "Matemática para los Negocios"), ("EAE24-003", "Introducción a la Contabilidad"), ("ETR24-001", "Intercomunicación Inicial"), ("ETR24-002", "Ofimática Inicial")],
                            [("EAE24-004", "Fundamentos de Marketing"), ("EAE24-005", "Matemática Financiera"), ("EAE24-006", "Contabilidad General"), ("ETR24-003", "Intercomunicación Avanzada"), ("ETR24-004", "Ofimática Avanzada")],
                            [("EAE24-007", "Fundamentos de Finanzas"), ("EAE24-008", "Investigación de Mercados"), ("EAE24-009", "Derecho Empresarial"), ("EAE24-010", "Estadística General"), ("ETR24-005", "Psicología Organizacional"), ("ETR24-010", "Introducción a la Ética")],
                            [("EAE24-011", "Elaboración de Procesos"), ("EAE24-012", "Costos y Presupuestos"), ("EAE24-013", "Análisis Cuantitativo para los Negocios"), ("EAE24-014", "Estadística para los Negocios"), ("ETR24-006", "Autorealización Personal"), ("ETR24-011", "Ética Profesional")],
                            [("EAE24-015", "Derecho Laboral"), ("EAE24-016", "Finanzas Empresariales"), ("EAE24-017", "Administración de Operaciones"), ("ETR24-007", "Atención al usuario"), ("ETR24-012", "Didáctica del Razonamiento"), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I")],
                            [("EAE24-018", "Talento Humano"), ("EAE24-019", "Comportamiento Humano en las Organizaciones"), ("EAE24-020", "Contabilidad Gerencial"), ("ETR24-008", "Sistema de medición de la atención al usuario"), ("ETR24-013", "Analisis de Situaciones Reales"), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II")],
                            [("EAE24-021", "Administración Estratégica"), ("EAE24-022", "Evaluación y Gestión de Proyectos"), ("EAE24-023", "Cadena de suministro"), ("ETR24-014", "Introducción a la Innovación"), ("ETR24-019", "Desarrollo Emprendedor"), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III")],
                            [("EAE24-024", "Estrategia Comercial"), ("EAE24-025", "Micro y Pequeña Empresa"), ("ETR24-009", "Plan de Negocios"), ("ETR24-015", "Innovación en productos y servicios"), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV")],
                            [("EAE24-026", "Marketing Estratégico"), ("EAE24-027", "Administración Pública"), ("EAE24-028", "E-business y Transformación Digital en las Empresas"), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V")],
                            [("ETR24-016", "Fundamentos de Investigación Aplicada"), ("ETR24-017", "Técnicas de Investigación Aplicada"), ("ETR24-018", "Seminario de Tesis"), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI")]
                        ]
                    },
                    "INGENIERIA DE SISTEMAS DE INFORMACIÓN": {
                        "codigo_base": "II",
                        "ciclos": [
                            [("EIS24-001", "Arquitectura Web"), ("EIS24-002", "Introducción a la Programación"), ("EIS24-003", "Matemática Aplicada"), ("ETR24-001", "Intercomunicación Inicial"), ("ETR24-002", "Ofimática Inicial")],
                            [("EIS24-004", "Fundamentos de Algoritmia"), ("EIS24-005", "Configuración de Aplicaciones"), ("EIS24-006", "Introducción al Modelamiento de Procesos"), ("ETR24-003", "Intercomunicación Avanzada"), ("ETR24-004", "Ofimática Avanzada")],
                            [("EIS24-007", "Fundamentos de Estructura de Datos"), ("EIS24-008", "Estadística Aplicada"), ("EIS24-009", "Diseño de Sistemas en TI"), ("EIS24-010", "Modelado de procesos en TI"), ("ETR24-005", "Psicología Organizacional"), ("ETR24-010", "Introducción a la Ética")],
                            [("EIS24-011", "Cyberseguridad"), ("EIS24-012", "Gestión de Servicios en TI"), ("EIS24-013", "Lenguaje de Programación"), ("EIS24-014", "Programación orientada a Objetos"), ("ETR24-006", "Autorealización Personal"), ("ETR24-011", "Ética Profesional")],
                            [("EIS24-015", "Arquitectura de sistemas operativos"), ("EIS24-016", "Programación de aplicaciones web"), ("EIS24-017", "Sistemas Distribuidos"), ("ETR24-007", "Atención al usuario"), ("ETR24-012", "Didáctica del Razonamiento"), ("ETR24-020", "Experiencia Formativa en Situación Real de Trabajo I")],
                            [("EIS24-018", "Soluciones móviles y cloud"), ("EIS24-019", "Modelamiento y análisis de sistemas"), ("EIS24-020", "Legislación en sistemas de información"), ("ETR24-013", "Analisis de Situaciones Reales"), ("ETR24-021", "Experiencia Formativa en Situación Real de Trabajo II")],
                            [("EIS24-021", "Arquitectura de software"), ("EIS24-022", "Modelamiento de base de datos"), ("EIS24-023", "Validación y pruebas de software"), ("ETR24-008", "Sistema de medición de la atención al usuario"), ("ETR24-014", "Introducción a la Innovación"), ("ETR24-022", "Experiencia Formativa en Situación Real de Trabajo III")],
                            [("EIS24-024", "Auditoría de sistemas"), ("EIS24-025", "Analítica con Big Data"), ("EIS24-026", "Inteligencia artificial"), ("ETR24-015", "Innovación en productos y servicios"), ("ETR24-023", "Experiencia Formativa en Situación Real de Trabajo IV")],
                            [("EIS24-027", "Bases de datos"), ("EIS24-028", "Proyectos en TI"), ("ETR24-009", "Plan de Negocios"), ("ETR24-019", "Desarrollo Emprendedor"), ("ETR24-024", "Experiencia Formativa en Situación Real de Trabajo V")],
                            [("ETR24-016", "Fundamentos de Investigación Aplicada"), ("ETR24-017", "Técnicas de Investigación Aplicada"), ("ETR24-018", "Seminario de Tesis"), ("ETR24-025", "Experiencia Formativa en Situación Real de Trabajo VI")]
                        ]
                    }
                }
            },
            "Instituto La Pontificia": {
                "carreras": {
                    "ADMINISTRACIÓN DE EMPRESAS": {
                        "codigo_base": "AEI",
                        "ciclos": [
                            [("AE23-001", "ADMINISTRACIÓN GENERAL"), ("AE23-002", "INTERCOMUNICACIÓN INICIAL"), ("AE23-003", "INTRODUCCIÓN A LA CONTABILIDAD"), ("AE23-004", "FUNDAMENTOS DE MARKETING"), ("AE23-005", "OFIMÁTICA INICIAL"), ("AE23-006", "MATEMÁTICA PARA LOS NEGOCIOS I")],
                            [("AE23-007", "INTERCOMUNICACIÓN AVANZADA"), ("AE23-008", "CONTABILIDAD FINANCIERA"), ("AE23-009", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I"), ("AE23-010", "OFIMÁTICA AVANZADA"), ("AE23-011", "MARKETING ESTRATÉGICO"), ("AE23-012", "MATEMÁTICA PARA LOS NEGOCIOS II")],
                            [("AE23-013", "ADMINISTRACIÓN ESTRATÉGICA I"), ("AE23-014", "COMPORTAMIENTO HUMANO EN LAS ORGANIZACIONES"), ("AE23-015", "AUTOREALIZACIÓN Y ÉTICA"), ("AE23-016", "CONTABILIDAD DE COSTOS"), ("AE23-017", "SERVICIO Y ATENCIÓN AL CLIENTE"), ("AE23-018", "ESTADÍSTICA APLICADA")],
                            [("AE23-019", "ADMINISTRACIÓN DE OPERACIONES"), ("AE23-020", "DERECHO EMPRESARIAL"), ("AE23-021", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL"), ("AE23-022", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II"), ("AE23-023", "FUNDAMENTOS DE FINANZAS"), ("AE23-024", "INDUCCIÓN AL MERCADO LABORAL")],
                            [("AE23-025", "DERECHO LABORAL Y TRIBUTARIO"), ("AE23-026", "E-BUSINESS Y TRANSFORMACIÓN DIGITAL EN LAS EMPRESAS"), ("AE23-027", "INVESTIGACIÓN DE MERCADOS"), ("AE23-028", "GESTIÓN DEL TALENTO HUMANO"), ("AE23-029", "MACRO Y MICRO ECONOMÍA"), ("AE23-030", "LIDERAZGO Y TRABAJO EN EQUIPO")],
                            [("AE23-031", "ADMINISTRACIÓN PÚBLICA"), ("AE23-032", "EVALUACIÓN Y GESTIÓN DE PROYECTOS"), ("AE23-033", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III"), ("AE23-034", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES"), ("AE23-035", "PLAN DE NEGOCIOS"), ("AE23-036", "ADQUISICIÓN DE BIENES Y SERVICIOS PÚBLICOS")]
                        ]
                    },
                    "CONTABILIDAD": {
                        "codigo_base": "CT",
                        "ciclos": [
                            [("CT23-001", "ADMINISTRACIÓN GENERAL"), ("CT23-002", "INTERCOMUNICACIÓN INICIAL"), ("CT23-003", "FUNDAMENTOS DE MARKETING"), ("CT23-004", "OFIMÁTICA INICIAL"), ("CT23-005", "INTRODUCCIÓN A LA CONTABILIDAD"), ("CT23-006", "MATEMÁTICA PARA LOS NEGOCIOS I")],
                            [("CT23-007", "INTERCOMUNICACIÓN AVANZADA"), ("CT23-008", "CONTABILIDAD DE COSTOS"), ("CT23-009", "CONTABILIDAD FINANCIERA I"), ("CT23-010", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I"), ("CT23-011", "OFIMÁTICA AVANZADA"), ("CT23-012", "MATEMÁTICA PARA LOS NEGOCIOS II")],
                            [("CT23-013", "CONTABILIDAD FINANCIERA II"), ("CT23-014", "DERECHO CIVIL Y COMERCIAL"), ("CT23-015", "DERECHO TRIBUTARIO"), ("CT23-016", "AUTOREALIZACIÓN Y ÉTICA"), ("CT23-017", "FUNDAMENTOS DE FINANZAS"), ("CT23-018", "MICROECONOMÍA PARA LOS NEGOCIOS")],
                            [("CT23-019", "ANÁLISIS Y REPORTES CONTABLES FINANCIEROS"), ("CT23-020", "CONTABILIDAD FINANCIERA III"), ("CT23-021", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL"), ("CT23-022", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II"), ("CT23-023", "FINANZAS CORPORATIVAS"), ("CT23-024", "TRIBUTACIÓN APLICADA I")],
                            [("CT23-025", "AUDITORÍA FINANCIERA"), ("CT23-026", "CONTABILIDAD GERENCIAL"), ("CT23-027", "DERECHO LABORAL Y TRIBUTARIO"), ("CT23-028", "AUDITORÍA Y CONTROL INTERNO"), ("CT23-029", "LIDERAZGO Y TRABAJO EN EQUIPO"), ("CT23-030", "TRIBUTACIÓN APLICADA II")],
                            [("CT23-031", "ADMINISTRACIÓN PÚBLICA"), ("CT23-032", "AUDITORÍA TRIBUTARIA"), ("CT23-033", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES"), ("CT23-034", "CONTABILIDAD GUBERNAMENTAL"), ("CT23-035", "EVALUACIÓN Y GESTIÓN DE PROYECTOS"), ("CT23-036", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III")]
                        ]
                    },
                    "ENFERMERIA TÉCNICA": {
                        "codigo_base": "ET",
                        "ciclos": [
                            [("ET23-001", "ANATOMÍA Y FISIOLOGÍA"), ("ET23-002", "SALUD COMUNITARIA"), ("ET23-003", "INTERCOMUNICACIÓN INICIAL"), ("ET23-004", "OFIMÁTICA INICIAL"), ("ET23-006", "PRIMEROS AUXILIOS")],
                            [("ET23-007", "BIOLOGÍA"), ("ET23-008", "INTERCOMUNICACIÓN AVANZADA"), ("ET23-009", "ENFERMERÍA BÁSICA I"), ("ET23-010", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO I"), ("ET23-011", "TERMINOLOGÍA EN SALUD"), ("ET23-012", "OFIMÁTICA AVANZADA")],
                            [("ET23-013", "ADMINISTRACIÓN DE MEDICAMENTOS"), ("ET23-014", "AUTOREALIZACIÓN Y ÉTICA"), ("ET23-015", "ENFERMERÍA BÁSICA II"), ("ET23-016", "EPIDEMIOLOGÍA"), ("ET23-017", "BIOSEGURIDAD"), ("ET23-018", "FARMACOLOGÍA")],
                            [("ET23-019", "ASISTENCIA EN INMUNIZACIONES"), ("ET23-020", "ASISTENCIA EN SALUD MATERNA Y DEL NEONATO"), ("ET23-021", "ASISTENCIA QUIRURGICA"), ("ET23-022", "SOSTENIBILIDAD Y RESPONSABILIDAD SOCIAL AMBIENTAL"), ("ET23-023", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO II"), ("ET23-024", "SALUD PÚBLICA"), ("ET23-037", "ASISTENCIA EN NEUMOLOGÍA")],
                            [("ET23-025", "ASISTENCIA EN FISIOTERAPIA Y REHABILITACIÓN"), ("ET23-026", "ASISTENCIA EN MEDICINA ALTERNATIVA"), ("ET23-027", "ASISTENCIA EN SALUD BUCAL"), ("ET23-028", "LIDERAZGO Y TRABAJO EN EQUIPO"), ("ET23-029", "SALUD DEL NIÑO Y DEL ADOLESCENTE"), ("ET23-030", "SALUD OCUPACIONAL")],
                            [("ET23-031", "ASISTENCIA AL PACIENTE ONCOLOGICO Y CUIDADOS PALIATIVOS"), ("ET23-032", "ASISTENCIA EN PROCEDIMIENTOS INVASIVOS Y NO INVASIVOS"), ("ET23-033", "ASISTENCIA EN SALUD MENTAL Y PSIQUIATRIA"), ("ET23-034", "ASISTENCIA GERIATRICA Y DEL ADULTO MAYOR"), ("ET23-035", "EXPERIENCIAS FORMATIVAS EN SITUACIONES REALES DE TRABAJO III"), ("ET23-036", "INNOVACIÓN Y DESARROLLO DE EMPRENDIMIENTOS PERSONALES")]
                        ]
                    }
                }
            }
        }

        # Crear grupos para cada ciclo de cada carrera
        for unidad_nombre, unidad_datos in DATOS_ACADEMICOS.items():
            for carrera_nombre, carrera_datos in unidad_datos['carreras'].items():
                # Obtener la carrera por código
                try:
                    carrera = Carrera.objects.get(codigo_carrera=carrera_datos['codigo_base'])
                    self.stdout.write(f'Procesando carrera: {carrera_nombre} ({carrera.codigo_carrera})')
                    
                    # Procesar cada ciclo
                    for i, ciclo_materias in enumerate(carrera_datos['ciclos'], 1):
                        # Obtener o crear el ciclo
                        ciclo, created = Ciclo.objects.get_or_create(
                            nombre_ciclo=f"Ciclo {i}",
                            orden=i,
                            carrera=carrera
                        )
                        
                        if created:
                            self.stdout.write(f'  ✓ Ciclo {i} creado para {carrera_nombre}')
                        
                        # Crear grupo para este ciclo
                        grupo, created = Grupos.objects.get_or_create(
                            codigo_grupo=f"{carrera.codigo_carrera}-{i}",
                            defaults={
                                'carrera': carrera,
                                'periodo': periodo_activo,
                                'numero_estudiantes_estimado': 30,
                                'turno_preferente': 'M',
                                'ciclo_semestral': i
                            }
                        )
                        
                        if created:
                            self.stdout.write(f'  ✓ Grupo {grupo.codigo_grupo} creado')
                        
                        # Asignar materias al grupo
                        materias_asignadas = 0
                        for codigo, nombre in ciclo_materias:
                            try:
                                materia = Materias.objects.get(codigo_materia=codigo)
                                grupo.materias.add(materia)
                                materias_asignadas += 1
                            except Materias.DoesNotExist:
                                self.stdout.write(f'    ⚠ Materia no encontrada: {codigo} - {nombre}')
                        
                        self.stdout.write(f'  ✓ {materias_asignadas} materias asignadas al ciclo {i}')
                        
                except Carrera.DoesNotExist:
                    self.stdout.write(f'❌ Carrera no encontrada: {carrera_nombre} (código: {carrera_datos["codigo_base"]})')
                except Carrera.MultipleObjectsReturned:
                    self.stdout.write(f'❌ Múltiples carreras encontradas para: {carrera_nombre} (código: {carrera_datos["codigo_base"]})')

        self.stdout.write(self.style.SUCCESS('¡Asignación de materias completada!'))
        
        # Mostrar resumen
        total_grupos = Grupos.objects.count()
        total_materias_asignadas = sum([g.materias.count() for g in Grupos.objects.all()])
        
        self.stdout.write(f'RESUMEN:')
        self.stdout.write(f'- Total grupos creados: {total_grupos}')
        self.stdout.write(f'- Total materias asignadas: {total_materias_asignadas}')
        
        # Mostrar grupos por carrera
        for carrera in Carrera.objects.all():
            grupos_carrera = Grupos.objects.filter(carrera=carrera)
            materias_carrera = sum([g.materias.count() for g in grupos_carrera])
            self.stdout.write(f'- {carrera.nombre_carrera}: {grupos_carrera.count()} grupos, {materias_carrera} materias') 