from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Resource, Subject

# Create your views here.


class ResourceList(generic.ListView):
    """
    Class based view to show an ordered list of resources
    """

    queryset = Resource.objects.filter(status="p")
    template_name = "resources/index.html"
    paginate_by = 6

    def get_context(self, **kwargs):
        context = super.get_context_data(**kwargs)
        print(f"context: {context}")
        page_obj = context.get("page_obj")

        return context


class ResourceDetail(generic.DetailView):

    model = Resource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

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


class SubjetResourceListView(generic.ListView):

    model = Resource
    template_name = "resources/subject_resource_list.html"
    context_object_name = "resources"

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
