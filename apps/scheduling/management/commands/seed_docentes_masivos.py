from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from apps.users.models import Docentes
from apps.scheduling.models import DisponibilidadDocentes, BloquesHorariosDefinicion
from apps.academic_setup.models import PeriodoAcademico, UnidadAcademica, Especialidades
import random
from datetime import time

class Command(BaseCommand):
    help = 'Crea 100 usuarios docentes con disponibilidades y datos completos para pruebas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--periodo',
            type=int,
            help='ID del período académico para asignar disponibilidades',
        )
        parser.add_argument(
            '--unidad',
            type=int,
            help='ID de la unidad académica para asignar docentes',
        )
        parser.add_argument(
            '--especialidades',
            type=str,
            nargs='+',
            help='IDs de especialidades separadas por espacios',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de 100 docentes...'))
        
        # Obtener período activo si no se especifica
        periodo_id = options['periodo']
        if not periodo_id:
            periodo = PeriodoAcademico.objects.filter(activo=True).first()
            if not periodo:
                self.stdout.write(self.style.ERROR('No hay períodos activos. Crea uno primero.'))
                return
            periodo_id = periodo.periodo_id
        else:
            try:
                periodo = PeriodoAcademico.objects.get(periodo_id=periodo_id)
            except PeriodoAcademico.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Período con ID {periodo_id} no encontrado.'))
                return

        # Obtener unidad académica si no se especifica
        unidad_id = options['unidad']
        if not unidad_id:
            unidad = UnidadAcademica.objects.first()
            if not unidad:
                self.stdout.write(self.style.ERROR('No hay unidades académicas. Crea una primero.'))
                return
            unidad_id = unidad.unidad_id
        else:
            try:
                unidad = UnidadAcademica.objects.get(unidad_id=unidad_id)
            except UnidadAcademica.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Unidad con ID {unidad_id} no encontrada.'))
                return

        # Obtener especialidades
        especialidades_ids = options['especialidades']
        if especialidades_ids:
            especialidades = Especialidades.objects.filter(especialidad_id__in=especialidades_ids)
        else:
            especialidades = list(Especialidades.objects.all())
        
        if not especialidades:
            self.stdout.write(self.style.ERROR('No hay especialidades disponibles. Crea algunas primero.'))
            return

        # Obtener grupo de docentes
        grupo_docentes, created = Group.objects.get_or_create(name='Docentes')
        
        # Obtener bloques horarios
        bloques = list(BloquesHorariosDefinicion.objects.all())
        if not bloques:
            self.stdout.write(self.style.ERROR('No hay bloques horarios definidos. Ejecuta crear_bloques_horarios primero.'))
            return

        # Datos de los 100 docentes
        docentes_data = [
            {"first_name": "Carlos", "last_name": "Martínez", "email": "carlos.martinez1@email.com"},
            {"first_name": "María", "last_name": "García", "email": "maria.garcia2@email.com"},
            {"first_name": "Juan", "last_name": "Pérez", "email": "juan.perez3@email.com"},
            {"first_name": "Ana", "last_name": "López", "email": "ana.lopez4@email.com"},
            {"first_name": "José", "last_name": "González", "email": "jose.gonzalez5@email.com"},
            {"first_name": "Laura", "last_name": "Sánchez", "email": "laura.sanchez6@email.com"},
            {"first_name": "David", "last_name": "Fernández", "email": "david.fernandez7@email.com"},
            {"first_name": "Lucía", "last_name": "Gómez", "email": "lucia.gomez8@email.com"},
            {"first_name": "Francisco", "last_name": "Díaz", "email": "francisco.diaz9@email.com"},
            {"first_name": "Elena", "last_name": "Torres", "email": "elena.torres10@email.com"},
            {"first_name": "Sergio", "last_name": "Ramírez", "email": "sergio.ramirez11@email.com"},
            {"first_name": "Paula", "last_name": "Flores", "email": "paula.flores12@email.com"},
            {"first_name": "Jorge", "last_name": "Moreno", "email": "jorge.moreno13@email.com"},
            {"first_name": "Alba", "last_name": "Navarro", "email": "alba.navarro14@email.com"},
            {"first_name": "Miguel", "last_name": "Santos", "email": "miguel.santos15@email.com"},
            {"first_name": "Sara", "last_name": "Ruiz", "email": "sara.ruiz16@email.com"},
            {"first_name": "Adrián", "last_name": "Molina", "email": "adrian.molina17@email.com"},
            {"first_name": "Patricia", "last_name": "Ortega", "email": "patricia.ortega18@email.com"},
            {"first_name": "Alejandro", "last_name": "Ramos", "email": "alejandro.ramos19@email.com"},
            {"first_name": "Marta", "last_name": "Vázquez", "email": "marta.vazquez20@email.com"},
            {"first_name": "Pablo", "last_name": "Castillo", "email": "pablo.castillo21@email.com"},
            {"first_name": "Alicia", "last_name": "Rivera", "email": "alicia.rivera22@email.com"},
            {"first_name": "Daniel", "last_name": "Silva", "email": "daniel.silva23@email.com"},
            {"first_name": "Nuria", "last_name": "Méndez", "email": "nuria.mendez24@email.com"},
            {"first_name": "Víctor", "last_name": "Cabrera", "email": "victor.cabrera25@email.com"},
            {"first_name": "Cristina", "last_name": "Hernández", "email": "cristina.hernandez26@email.com"},
            {"first_name": "Óscar", "last_name": "Iglesias", "email": "oscar.iglesias27@email.com"},
            {"first_name": "Raquel", "last_name": "Martín", "email": "raquel.martin28@email.com"},
            {"first_name": "Manuel", "last_name": "Suárez", "email": "manuel.suarez29@email.com"},
            {"first_name": "Eva", "last_name": "Rodríguez", "email": "eva.rodriguez30@email.com"},
            {"first_name": "Roberto", "last_name": "Jiménez", "email": "roberto.jimenez31@email.com"},
            {"first_name": "Isabel", "last_name": "Morales", "email": "isabel.morales32@email.com"},
            {"first_name": "Antonio", "last_name": "Reyes", "email": "antonio.reyes33@email.com"},
            {"first_name": "Carmen", "last_name": "Vega", "email": "carmen.vega34@email.com"},
            {"first_name": "Eduardo", "last_name": "Cruz", "email": "eduardo.cruz35@email.com"},
            {"first_name": "Mónica", "last_name": "Medina", "email": "monica.medina36@email.com"},
            {"first_name": "Fernando", "last_name": "Aguilar", "email": "fernando.aguilar37@email.com"},
            {"first_name": "Silvia", "last_name": "Herrera", "email": "silvia.herrera38@email.com"},
            {"first_name": "Gabriel", "last_name": "Romero", "email": "gabriel.romero39@email.com"},
            {"first_name": "Beatriz", "last_name": "Ríos", "email": "beatriz.rios40@email.com"},
            {"first_name": "Ricardo", "last_name": "Espinoza", "email": "ricardo.espinoza41@email.com"},
            {"first_name": "Diana", "last_name": "Contreras", "email": "diana.contreras42@email.com"},
            {"first_name": "Hugo", "last_name": "Valdez", "email": "hugo.valdez43@email.com"},
            {"first_name": "Verónica", "last_name": "Mendoza", "email": "veronica.mendoza44@email.com"},
            {"first_name": "Arturo", "last_name": "León", "email": "arturo.leon45@email.com"},
            {"first_name": "Graciela", "last_name": "Ríos", "email": "graciela.rios46@email.com"},
            {"first_name": "Federico", "last_name": "Campos", "email": "federico.campos47@email.com"},
            {"first_name": "Rosario", "last_name": "Aguirre", "email": "rosario.aguirre48@email.com"},
            {"first_name": "Sebastián", "last_name": "Vélez", "email": "sebastian.velez49@email.com"},
            {"first_name": "Adriana", "last_name": "Quintero", "email": "adriana.quintero50@email.com"},
            {"first_name": "Rodrigo", "last_name": "Ospina", "email": "rodrigo.ospina51@email.com"},
            {"first_name": "Lorena", "last_name": "Parra", "email": "lorena.parra52@email.com"},
            {"first_name": "Felipe", "last_name": "Escobar", "email": "felipe.escobar53@email.com"},
            {"first_name": "Claudia", "last_name": "Uribe", "email": "claudia.uribe54@email.com"},
            {"first_name": "Marcelo", "last_name": "Arias", "email": "marcelo.arias55@email.com"},
            {"first_name": "Valentina", "last_name": "Mejía", "email": "valentina.mejia56@email.com"},
            {"first_name": "Nicolás", "last_name": "Bernal", "email": "nicolas.bernal57@email.com"},
            {"first_name": "Camila", "last_name": "Rodríguez", "email": "camila.rodriguez58@email.com"},
            {"first_name": "Andrés", "last_name": "Montoya", "email": "andres.montoya59@email.com"},
            {"first_name": "Sofía", "last_name": "Giraldo", "email": "sofia.giraldo60@email.com"},
            {"first_name": "Santiago", "last_name": "Ochoa", "email": "santiago.ochoa61@email.com"},
            {"first_name": "Daniela", "last_name": "Herrera", "email": "daniela.herrera62@email.com"},
            {"first_name": "Julián", "last_name": "Vásquez", "email": "julian.vasquez63@email.com"},
            {"first_name": "Mariana", "last_name": "Ortiz", "email": "mariana.ortiz64@email.com"},
            {"first_name": "Tomás", "last_name": "Guzmán", "email": "tomas.guzman65@email.com"},
            {"first_name": "Lucía", "last_name": "Morales", "email": "lucia.morales66@email.com"},
            {"first_name": "Mateo", "last_name": "Cárdenas", "email": "mateo.cardenas67@email.com"},
            {"first_name": "Isabella", "last_name": "Ramírez", "email": "isabella.ramirez68@email.com"},
            {"first_name": "Benjamín", "last_name": "Torres", "email": "benjamin.torres69@email.com"},
            {"first_name": "Emma", "last_name": "Flores", "email": "emma.flores70@email.com"},
            {"first_name": "Lucas", "last_name": "Silva", "email": "lucas.silva71@email.com"},
            {"first_name": "Valeria", "last_name": "Castro", "email": "valeria.castro72@email.com"},
            {"first_name": "Diego", "last_name": "Mendoza", "email": "diego.mendoza73@email.com"},
            {"first_name": "Renata", "last_name": "Vega", "email": "renata.vega74@email.com"},
            {"first_name": "Maximiliano", "last_name": "Ruiz", "email": "maximiliano.ruiz75@email.com"},
            {"first_name": "Antonia", "last_name": "Moreno", "email": "antonia.moreno76@email.com"},
            {"first_name": "Agustín", "last_name": "Navarro", "email": "agustin.navarro77@email.com"},
            {"first_name": "Constanza", "last_name": "Medina", "email": "constanza.medina78@email.com"},
            {"first_name": "Joaquín", "last_name": "Reyes", "email": "joaquin.reyes79@email.com"},
            {"first_name": "Catalina", "last_name": "Ortega", "email": "catalina.ortega80@email.com"},
            {"first_name": "Ignacio", "last_name": "Cabrera", "email": "ignacio.cabrera81@email.com"},
            {"first_name": "Florencia", "last_name": "Espinoza", "email": "florencia.espinoza82@email.com"},
            {"first_name": "Vicente", "last_name": "Contreras", "email": "vicente.contreras83@email.com"},
            {"first_name": "Josefina", "last_name": "Valdez", "email": "josefina.valdez84@email.com"},
            {"first_name": "Rafael", "last_name": "León", "email": "rafael.leon85@email.com"},
            {"first_name": "Gabriela", "last_name": "Campos", "email": "gabriela.campos86@email.com"},
            {"first_name": "Cristóbal", "last_name": "Vélez", "email": "cristobal.velez87@email.com"},
            {"first_name": "Trinidad", "last_name": "Quintero", "email": "trinidad.quintero88@email.com"},
            {"first_name": "Matías", "last_name": "Ospina", "email": "matias.ospina89@email.com"},
            {"first_name": "Amanda", "last_name": "Parra", "email": "amanda.parra90@email.com"},
            {"first_name": "Bautista", "last_name": "Escobar", "email": "bautista.escobar91@email.com"},
            {"first_name": "Carmen", "last_name": "Uribe", "email": "carmen.uribe92@email.com"},
            {"first_name": "Dante", "last_name": "Arias", "email": "dante.arias93@email.com"},
            {"first_name": "Celeste", "last_name": "Mejía", "email": "celeste.mejia94@email.com"},
            {"first_name": "Enzo", "last_name": "Bernal", "email": "enzo.bernal95@email.com"},
            {"first_name": "Luna", "last_name": "Montoya", "email": "luna.montoya96@email.com"},
            {"first_name": "Thiago", "last_name": "Giraldo", "email": "thiago.giraldo97@email.com"},
            {"first_name": "Alma", "last_name": "Ochoa", "email": "alma.ochoa98@email.com"},
            {"first_name": "Axel", "last_name": "Vásquez", "email": "axel.vasquez99@email.com"},
            {"first_name": "Maya", "last_name": "Ortiz", "email": "maya.ortiz100@email.com"},
        ]

        with transaction.atomic():
            docentes_creados = 0
            disponibilidades_creadas = 0

            for i, docente_data in enumerate(docentes_data, 1):
                username = f"usuario{i}"
                
                # Verificar si el usuario ya existe
                if User.objects.filter(username=username).exists():
                    self.stdout.write(f'Usuario {username} ya existe, saltando...')
                    continue

                try:
                    # Crear usuario
                    user = User.objects.create_user(
                        username=username,
                        email=docente_data['email'],
                        first_name=docente_data['first_name'],
                        last_name=docente_data['last_name'],
                        password='123456',
                        is_active=True
                    )
                    user.groups.add(grupo_docentes)

                    # Crear docente
                    docente = Docentes.objects.create(
                        usuario=user,
                        codigo_docente=f"DOC{i:03d}",
                        nombres=docente_data['first_name'],
                        apellidos=docente_data['last_name'],
                        email=docente_data['email'],
                        telefono=f"300{random.randint(1000000, 9999999)}",
                        unidad_principal=unidad
                    )

                    # Asignar especialidades aleatorias (1-3 especialidades por docente)
                    num_especialidades = random.randint(1, min(3, len(especialidades)))
                    especialidades_aleatorias = random.sample(especialidades, num_especialidades)
                    docente.especialidades.set(especialidades_aleatorias)

                    # Crear disponibilidades
                    for bloque in bloques:
                        # 70% de probabilidad de estar disponible
                        esta_disponible = random.random() < 0.7
                        
                        if esta_disponible:
                            # Preferencia aleatoria: -2 (no preferido) a 3 (muy preferido)
                            preferencia = random.randint(-2, 3)
                        else:
                            preferencia = -999  # No disponible

                        DisponibilidadDocentes.objects.create(
                            docente=docente,
                            periodo=periodo,
                            dia_semana=bloque.dia_semana,
                            bloque_horario=bloque,
                            esta_disponible=esta_disponible,
                            preferencia=preferencia
                        )
                        disponibilidades_creadas += 1

                    docentes_creados += 1
                    self.stdout.write(f'Creado docente {i}/100: {docente_data["first_name"]} {docente_data["last_name"]}')

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creando docente {i}: {str(e)}'))
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Proceso completado. Creados {docentes_creados} docentes con {disponibilidades_creadas} disponibilidades.'
        ))
        self.stdout.write(f'Período: {periodo.nombre_periodo}')
        self.stdout.write(f'Unidad: {unidad.nombre_unidad}')
        self.stdout.write(f'Especialidades asignadas: {[e.nombre_especialidad for e in especialidades]}') 