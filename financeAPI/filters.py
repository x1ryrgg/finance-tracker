import django_filters
from financeAPI.models import *

class ObjectFilter(django_filters.FilterSet):
    object = django_filters.CharFilter(field_name='object', lookup_expr='icontains', label='Название содержит')
    obj_money__gt = django_filters.NumberFilter(field_name='obj_money', lookup_expr='gt', label='Сумма больше чем')
    obj_money__lt = django_filters.NumberFilter(field_name='obj_money', lookup_expr='lt', label='Сумма меньше чем')
    class Meta:
        model = Objective
        fields = ()