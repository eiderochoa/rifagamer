from rest_framework import serializers
from .models import *

class RifaSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()
    class Meta:
        model = Rifa
        fields = '__all__'