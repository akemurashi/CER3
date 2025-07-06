from rest_framework import serializers
from .models import Taller, Categoria, Profesor, Lugar

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['id', 'nombre_completo']

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ['id', 'nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class TallerSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True)
    lugar = LugarSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Taller
        fields = '__all__'

class CrearTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        exclude = ['estado', 'observacion', 'creado_por']
