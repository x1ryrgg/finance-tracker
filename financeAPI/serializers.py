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
    all_money_test = serializers.SerializerMethodField() # создает новое поле на основе какого то поля из бд (get_all_money_test)
    class Meta:
        model = Profile
        fields = ['all_money', 'text', 'image', 'obj', 'all_money_test']

    def get_all_money_test(self, obj):
        all_money_test = obj.all_money * 0.25
        return all_money_test


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



