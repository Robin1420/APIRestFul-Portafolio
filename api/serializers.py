import base64
from rest_framework import serializers
from .models import (
    Certificados, DatosPersonales, Experiencias,
    Proyectos, RedesSociales, Skills, UsuariosAdmin
)


class CertificadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificados
        fields = '__all__'
        read_only_fields = ('id',)


class Base64FileField(serializers.Field):
    def to_representation(self, value):
        if value:
            import base64
            return base64.b64encode(value).decode('utf-8')
        return None

    def to_internal_value(self, data):
        if data is None or data == '':
            return None
        
        # Si es un diccionario (como cuando se envía desde el formulario web de DRF)
        if isinstance(data, dict) and 'file' in data:
            return data['file'].read()
            
        # Si se envía directamente el archivo
        if hasattr(data, 'read'):
            return data.read()
            
        # Si se envía como base64
        import base64
        try:
            if 'base64,' in data:
                # Manejar data URI (data:image/png;base64,...)
                data = data.split('base64,')[1]
            return base64.b64decode(data)
        except Exception:
            raise serializers.ValidationError("Formato de archivo no válido. Use base64 o envíe el archivo directamente.")


class DatosPersonalesSerializer(serializers.ModelSerializer):
    foto_perfil = Base64FileField(required=False, allow_null=True)
    cv = Base64FileField(required=False, allow_null=True)
    
    class Meta:
        model = DatosPersonales
        fields = [
            'id', 'nombre', 'profesion', 'descripcion', 'email',
            'telefono', 'direccion', 'foto_perfil', 'cv'
        ]
        read_only_fields = ('id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Para la foto de perfil
        if instance.foto_perfil:
            representation['foto_perfil'] = base64.b64encode(instance.foto_perfil).decode('utf-8')
        else:
            representation['foto_perfil'] = None
            
        # Para el CV
        if instance.cv:
            representation['cv'] = base64.b64encode(instance.cv).decode('utf-8')
        else:
            representation['cv'] = None
            
        return representation


class ExperienciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiencias
        fields = '__all__'
        read_only_fields = ('id',)


class ProyectosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyectos
        fields = '__all__'
        read_only_fields = ('id',)


class RedesSocialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedesSociales
        fields = '__all__'
        read_only_fields = ('id',)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'
        read_only_fields = ('id',)


class UsuariosAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuariosAdmin
        fields = ['id', 'username', 'email', 'creado_en']
        read_only_fields = ('id', 'creado_en')
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

    def create(self, validated_data):
        user = UsuariosAdmin.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password_hash'],
            email=validated_data.get('email', '')
        )
        return user