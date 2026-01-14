import django_filters as df
from django.db.models import Q, Count
from .models import Resource, Subject


class ResourceFilter(df.FilterSet):
    """
    FilterSet for narrowing the Resource list view.

    This filterset supports:
    - Keyword-based searching on resource titles.
    - Subject-based filtering using both free-text matching and
      multi-select AND semantics.
    - Date-based filtering using predefined ranges (e.g. today, past week).

    Filtering logic is encapsulated here to keep view logic minimal
    and to allow filter behaviour to evolve independently of views.
    """

    title = df.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )

    subjects_single = df.CharFilter(
        field_name="subjects__name",
        lookup_expr="icontains",
        label="Subjects include",
    )

    subjects = df.ModelMultipleChoiceFilter(
        queryset=Subject.objects.order_by("name"),
        method="filter_subjects_and",
    )

    created_on = df.DateRangeFilter(
        field_name="created_on",
        label="Created on",
    )

    def filter_subjects_and(self, queryset, name, selected_subjects):
        """
        Apply AND-based subject filtering to the queryset.

        When multiple subjects are selected, only resources associated with
        *all* selected subjects are returned. This differs from the default
        OR behaviour provided by ModelMultipleChoiceFilter.

        This method conforms to the django-filter method-based filter
        signature: (self, queryset, name, value) -> QuerySet.

        Args:
            queryset (QuerySet): The current Resource queryset being filtered.
            name (str): The name of the filter field invoking this method.
            selected_subjects (QuerySet[Subject]): The validated set of
                Subject instances selected by the user.

        Returns:
            QuerySet: A queryset of Resource objects that include all
            selected subjects.
        """

        if not selected_subjects:
            return queryset

        selected_subject_ids = list(
            selected_subjects.values_list(
                "id",
                flat=True,
            )
        )
        selected_count = len(selected_count)

        # 1) Keep resources that have at least the selected subjects
        # 2) Count how many of the selected subjects each resource matches
        # 3) Only keep resources where the match count equals number selected

        return queryset.filter(subjects__in=selected_subject_ids).annotate(
            matched_subject_count=Count(
                "subjects", filter=Q(subjects__in=selected_subject_ids), distinct=True
            ).filter(matched_subject_count=selected_count)
        )

    class Meta:
        model = Resource
        exclude = ["featured_image"]
