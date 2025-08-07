import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, Region, City, District


class PropertyFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains', label="Город")
    district = django_filters.CharFilter(field_name='district__name', lookup_expr='icontains', label="Район")
    region = django_filters.CharFilter(field_name='region__name', lookup_expr='icontains', label="Регион")

    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label="Минимальная цена")
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label="Максимальная цена")

    property_type = django_filters.CharFilter(field_name='property_type', lookup_expr='icontains',
                                              label="Тип недвижимости")


    class Meta:
        model = Property
        fields = ['city', 'district', 'region', 'price_min', 'price_max', 'property_type']
