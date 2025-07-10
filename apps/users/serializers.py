#apps/users/serializers.py
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Docentes, Roles, DocenteEspecialidades # SesionesUsuario
from apps.academic_setup.serializers import EspecialidadesSerializer # Para anidar
from apps.users.models import Especialidades # Asegúrate de que Especialidades se importe correctamente
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GroupSerializer(serializers.ModelSerializer): # Para los grupos de Django
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True) # Muestra los grupos del usuario
    docente_email = serializers.SerializerMethodField(read_only=True)

    def get_docente_email(self, obj):
        if hasattr(obj, 'perfil_docente') and obj.perfil_docente and obj.perfil_docente.email:
            return obj.perfil_docente.email
        return None

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups', 'docente_email') #, 'perfil_docente_id')
        read_only_fields = ('is_staff', 'is_active', 'groups')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'groups']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este correo electrónico ya está en uso."})
        return data

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class DocenteEspecialidadesSimpleSerializer(serializers.ModelSerializer): # Para la lista dentro de Docente
    especialidad_id = serializers.IntegerField(source='especialidad.especialidad_id')
    nombre_especialidad = serializers.CharField(source='especialidad.nombre_especialidad', read_only=True)

    class Meta:
        model = DocenteEspecialidades
        fields = ['especialidad_id', 'nombre_especialidad']


class DocentesSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True, allow_null=True)
    unidad_principal_nombre = serializers.CharField(source='unidad_principal.nombre_unidad', read_only=True, allow_null=True)
    # Mostrar especialidades de forma más detallada o simple
    especialidades_detalle = EspecialidadesSerializer(source='especialidades', many=True, read_only=True) # ManyToManyField
    
    # Campo para recibir los IDs de las especialidades al crear/actualizar
    especialidades = serializers.PrimaryKeyRelatedField(
        queryset=Especialidades.objects.all(),
        many=True,
        write_only=True,
        required=False  # No es obligatorio que un docente tenga especialidades
    )


    class Meta:
        model = Docentes
        fields = ['docente_id', 'usuario', 'usuario_username', 'codigo_docente', 'nombres', 'apellidos', 'dni',
                  'email', 'telefono', 'tipo_contrato', 'max_horas_semanales',
                  'unidad_principal', 'unidad_principal_nombre', 'especialidades_detalle', 'especialidades']

    def create(self, validated_data):
        especialidades_data = validated_data.pop('especialidades', [])
        docente = Docentes.objects.create(**validated_data)
        docente.especialidades.set(especialidades_data)
        return docente

    def update(self, instance, validated_data):
        especialidades_data = validated_data.pop('especialidades', None)
        instance = super().update(instance, validated_data)
        # Solo actualiza si 'especialidades' fue incluido en la petición
        if especialidades_data is not None:
            instance.especialidades.set(especialidades_data)
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # Aquí podrías añadir un campo personalizado si lo necesitas en el token mismo
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': [group.name for group in user.groups.all()],
        }
        # Si el usuario es un docente y tiene un perfil de docente asociado
        if hasattr(user, 'perfil_docente') and user.perfil_docente:
            user_data['docente_id'] = user.perfil_docente.docente_id
            user_data['especialidades_nombres'] = [
                esp.nombre_especialidad for esp in user.perfil_docente.especialidades.all()
            ]

        data['user'] = user_data
        return data

class UserUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups']

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if groups is not None:
            instance.groups.set(groups)
        instance.save()
        return instance
    