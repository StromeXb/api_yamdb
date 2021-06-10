from django_filters import filters, rest_framework

from .models import Title


class TitleFilter(rest_framework.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
