from django.shortcuts import render
from django.views import generic
from .models import Resource

# Create your views here.


class ResourceList(generic.ListView):
    """
    Class based view to show an ordered list of resources
    """

    queryset = Resource.objects.filter(status=1)
    template_name = "resources/index.html"
    paginate_by = 6

    def get_context(self, **kwargs):
        context = super.get_context_data(**kwargs)
        page_obj = context.get("page_obj")

        return context

        # TODO: Add POST conditional branch for comment submission
