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
