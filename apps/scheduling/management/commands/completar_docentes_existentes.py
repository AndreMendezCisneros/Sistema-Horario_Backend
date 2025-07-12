from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from apps.users.models import Docentes
from apps.scheduling.models import DisponibilidadDocentes, BloquesHorariosDefinicion
from apps.academic_setup.models import PeriodoAcademico, UnidadAcademica, Especialidades
import random

class Command(BaseCommand):
    help = 'Completa los datos de docentes y disponibilidades para usuarios existentes'

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
        self.stdout.write(self.style.SUCCESS('Completando datos de docentes existentes...'))
        
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
        grupo_docentes = Group.objects.filter(name='Docentes').first()
        if not grupo_docentes:
            self.stdout.write(self.style.ERROR('No existe el grupo "Docentes".'))
            return
        
        # Obtener bloques horarios
        bloques = list(BloquesHorariosDefinicion.objects.all())
        if not bloques:
            self.stdout.write(self.style.ERROR('No hay bloques horarios definidos. Ejecuta crear_bloques_horarios primero.'))
            return

        # Obtener usuarios que están en el grupo de docentes pero no tienen registro de Docentes
        usuarios_docentes = User.objects.filter(groups=grupo_docentes)
        usuarios_sin_docente = []
        
        for usuario in usuarios_docentes:
            if not Docentes.objects.filter(usuario=usuario).exists():
                usuarios_sin_docente.append(usuario)

        if not usuarios_sin_docente:
            self.stdout.write(self.style.WARNING('Todos los usuarios docentes ya tienen registros de Docentes.'))
            return

        self.stdout.write(f'Encontrados {len(usuarios_sin_docente)} usuarios sin registros de Docentes.')

        with transaction.atomic():
            docentes_creados = 0
            disponibilidades_creadas = 0

            for usuario in usuarios_sin_docente:
                try:
                    # Extraer número del username (usuario1, usuario2, etc.)
                    username_num = usuario.username.replace('usuario', '')
                    if username_num.isdigit():
                        num = int(username_num)
                    else:
                        num = random.randint(100, 999)

                    # Crear docente
                    docente = Docentes.objects.create(
                        usuario=usuario,
                        codigo_docente=f"DOC{num:03d}",
                        nombres=usuario.first_name,
                        apellidos=usuario.last_name,
                        email=usuario.email,
                        telefono=f"300{random.randint(1000000, 9999999)}",
                        unidad_principal=unidad,
                        tipo_contrato="TC",
                        max_horas_semanales=40
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
                    self.stdout.write(f'Creado docente para {usuario.username}: {usuario.first_name} {usuario.last_name}')

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creando docente para {usuario.username}: {str(e)}'))
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Proceso completado. Creados {docentes_creados} docentes con {disponibilidades_creadas} disponibilidades.'
        ))
        self.stdout.write(f'Período: {periodo.nombre_periodo}')
        self.stdout.write(f'Unidad: {unidad.nombre_unidad}')
        self.stdout.write(f'Especialidades asignadas: {[e.nombre_especialidad for e in especialidades]}') 