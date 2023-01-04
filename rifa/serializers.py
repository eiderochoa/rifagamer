from rest_framework import serializers
from .models import *

class RifaSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()
    class Meta:
        model = Rifa
        fields = '__all__'

class NumerosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numeros
        fields = '__all__'

class BonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bono
        fields = '__all__'