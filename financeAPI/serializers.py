from .models import *
from rest_framework import serializers


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = "__all__"
        read_only_fields = ['time_create', 'time_update']


class OBJserializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ['obj_money', 'object']

class ProfileSerializer(serializers.ModelSerializer):
    obj = OBJserializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['all_money', 'text', 'image', 'obj']



