from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin
from .models import Resource, Subject

# Create your views here.


class ResourceList(
    ListBreadcrumbMixin,
    generic.ListView,
):
    """
    Class based view to show an ordered list of resources
    """

    model = Resource
    queryset = Resource.objects.filter(status="p")
    template_name = "resources/index.html"
    paginate_by = 6
    add_home = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"context: {context}")
        page_obj = context.get("page_obj")

        return context


class ResourceDetail(
    DetailBreadcrumbMixin,
    generic.DetailView,
):

    model = Resource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"
    add_home = False
    breadcrumb_use_pk = False

    def get_queryset(self):
        """
        Displays an individual :model:`resources.Resource`
        :param self: The class instance

        **Context**
            *All variables returned to the template*
        ``resource``
            An instance of :model:`resources.Resource`
        """
        resource = Resource.objects.filter(status="p")

        # TODO: Add POST and comment logic
        return resource


class SubjetResourceListView(
    ListBreadcrumbMixin,
    generic.ListView,
):

    model = Resource
    template_name = "resources/subject_resource_list.html"
    context_object_name = "resources"

    @property
    def crumbs(self):
        """
        crumbs property override to ensure it displays
        subject's name, not "Resources"
        """
        return [
            (
                self.subject.name,
                reverse(
                    "resources:subject_resource_list",
                    kwargs={"slug": self.subject.slug},
                ),
            )
        ]

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, slug=self.kwargs["slug"])

        return (
            Resource.objects.filter(
                subjects=self.subject,
                status="p",
            )
            .select_related("author")
            .prefetch_related("subjects")
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["subject"] = self.subject
        return context
