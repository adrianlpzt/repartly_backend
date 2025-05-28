# baseapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Platform, Entrega, Recogida, Gasto

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'fecha_nacimiento', 'telefono', 'notas', 'is_premium', 'fecha_registro', 'nif']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'nombre', 'precio_entrega', 'precio_recogida']

class EntregaSerializer(serializers.ModelSerializer):
    plataforma_nombre = serializers.CharField(source='plataforma.nombre', read_only=True)

    class Meta:
        model = Entrega
        fields = ['id', 'plataforma', 'plataforma_nombre', 'cantidad', 'fecha', 'observaciones', 'total']

class RecogidaSerializer(serializers.ModelSerializer):
    plataforma_nombre = serializers.CharField(source='plataforma.nombre', read_only=True)

    class Meta:
        model = Recogida
        fields = ['id', 'plataforma', 'plataforma_nombre', 'cantidad', 'fecha', 'observaciones', 'total']

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = ['id', 'concepto', 'cantidad', 'fecha', 'observaciones']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    telefono = serializers.CharField(write_only=True, required=False)
    nif = serializers.CharField(write_only=True, required=False)
    fecha_nacimiento = serializers.DateField(write_only=True, required=False)
    avatar = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'telefono', 'nif', 'fecha_nacimiento', 'avatar'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        telefono = validated_data.pop('telefono', '')
        nif = validated_data.pop('nif', '')
        fecha_nacimiento = validated_data.pop('fecha_nacimiento', None)
        avatar = validated_data.pop('avatar', None)

        # Crear usuario (inactivo)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.is_active = False
        user.save()

        # Crear perfil asociado
        Profile.objects.create(
            user=user,
            telefono=telefono,
            nif=nif,
            fecha_nacimiento=fecha_nacimiento,
            avatar=avatar
        )

        return user

