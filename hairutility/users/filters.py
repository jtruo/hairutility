from .models import HairProfile, User
from django_filters.rest_framework import filterset, CharFilter
from rest_framework.filters import BaseFilterBackend


class TagsFilter(CharFilter):

    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            qs = qs.filter(tags__name__in=tags).distinct()

        return qs


class HairProfileFilter(filterset.FilterSet):

    tags = TagsFilter(name="tags", lookup_expr='icontains')

    class Meta:

        model = HairProfile

        fields = {
            # 'created': ['exact', 'contains'],
            'is_displayable': ['exact'],
            'is_approved': ['exact'],
            'user__email': ['exact'],
            'access_code': ['exact']


        }
