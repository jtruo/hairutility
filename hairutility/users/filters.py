from .models import HairProfile
from django_filters.rest_framework import filterset, CharFilter


class TagsFilter(CharFilter):

    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            qs = qs.filter(tags__name__in=tags).distinct()

        return qs
# Would it be better to split gender and hair length into separate fields, and then tags separately queried?


class HairProfileFilter(filterset.FilterSet):

    tags = TagsFilter(field_name="tags", lookup_expr='icontains')

    class Meta:

        model = HairProfile

        fields = {
            # 'created': ['exact', 'contains'],
            'is_displayable': ['exact'],
            'is_approved': ['exact'],
            'user__email': ['exact'],
            'access_code': ['exact'],
            'gender': ['exact'],
            'length': ['exact'],

        }
