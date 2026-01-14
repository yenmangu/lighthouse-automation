import django_filters as df
from .models import Resource


class ResourceFilter(df.FilterSet):
    """
    Custom filterset, inheriting from django_filters package.
    TODO: Update as filters added.
    """

    title = df.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )

    subjects = df.CharFilter(
        field_name="subjects__name",
        lookup_expr="icontains",
        label="Subjects include",
    )

    created_on = df.DateRangeFilter(
        field_name="created_on",
        lookup_expr="date",
        label="Created on",
    )

    class Meta:
        model = Resource
        fields = []
