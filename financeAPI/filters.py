import django_filters
from financeAPI.models import *

class ObjectFilter(django_filters.FilterSet):
    class Meta:
        model = Objective
        fields = {'object': ['icontains'],
                  'obj_money': ['lt', 'gt'],
                  }