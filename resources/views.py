from typing import Any
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin
from .models import Resource, Subject
from .forms import CommentForm

# Create your views here.


class ResourceList(
    ListBreadcrumbMixin,
    generic.ListView,
):
    """
    Display the home page resource feed as a paginated list.

    The list is restricted to published resources and ordered according to the
    default ordering defined on the :model:`resources.Resource` model (if set).

    **Context**
    ``resource_list``
        The list of :model:`resources.Resource` objects for the current page.
        This name is provided by Django's ListView by default.

    ``page_obj``
        Pagination object for the current page.

    ``paginator``
        Paginator instance controlling pagination.

    ``is_paginated``
        Boolean indicating whether pagination is active.

    **Template**
    :template:`resources/index.html`
    """

    model = Resource
    queryset = Resource.objects.filter(status="p")
    template_name = "resources/index.html"
    paginate_by = 6
    add_home = False

    def get_context_data(self, **kwargs):
        """
        Extend the template context for the resource list page.

        This method currently prints the full context for debugging and extracts
        the ``page_obj`` (pagination) object. No additional keys are added yet,
        but this hook is the correct place to inject extra homepage context
        later (for example: hero copy, featured subjects, or site statistics).

        Args:
            **kwargs: Additional context provided by Django.

        Returns:
            dict: Context dictionary passed to the template.
        """
        context = super().get_context_data(**kwargs)
        print(f"context: {context}")
        page_obj = context.get("page_obj")

        return context


class ResourceDetail(
    DetailBreadcrumbMixin,
    generic.DetailView,
):
    """
    Display an individual published :model:`resources.Resource`
    and handle comment submission.

    This view supports GET and POST:

    - GET renders the resource detail page.
    - POST processes a submitted comment form for the displayed resource.

    **Context**
    ``resource``
        An instance of :model:`resources.Resource` (provided by DetailView).

    ``comments``
        Approved comments associated with the current :model:`resources.Resource`.

    ``comment_form``
        Form instance returned by :class:`CommentForm`, for leaving comments.

    **Template**
    :template:`resources/resource_detail.html`
    """

    model = Resource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"
    add_home = False
    breadcrumb_use_pk = False

    def get_queryset(self):
        """
        Restrict visible resources to published only.

        This ensures draft or withdrawn resources cannot be accessed directly,
        even if a user guesses the slug.

        Returns:
            QuerySet: Published :model:`resources.Resource` objects only.
        """
        resource = Resource.objects.filter(status="p")

        return resource

    def post(self, request: HttpRequest, **kwargs):
        """
        Handle POST requests for comment submission on a resource detail page.

        If the user is not authenticated, they are redirected to the allauth
        login page.

        If the submitted :class:`CommentForm` is valid, a new comment is created,
        linked to the current user and the displayed resource, and a success
        message is added. The user is then redirected back to the same detail
        page to prevent duplicate submissions on refresh.

        If the form is invalid, the detail page is re-rendered with the bound
        form so validation errors are displayed.

        Args:
            request (HttpRequest): The incoming HttpRequest object.

        Returns:
            HttpResponse: Redirect on success, or a rendered template response
            containing form errors on failure.
        """
        if not request.user.is_authenticated:
            return redirect("account_login")

        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.resource = self.object
            comment.save()

            messages.add_message(request, messages.SUCCESS, "Comment submitted!")
            return HttpResponseRedirect(
                reverse("resource_detail", kwargs={"slug": self.object.slug})
            )
        context = self.get_context_data(comment_form=comment_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Add comments and a comment form to the template context.

        Extends the default DetailView context with:

        - ``comments``: approved comments for the current resource
        - ``comment_form``: a blank form on GET, or a bound form on invalid POST

        Returns:
            dict: Context dictionary passed to the template.
        """
        context = super().get_context_data(**kwargs)

        context["comments"] = self.object.comments.filter(approved=True)
        context.setdefault("comment_form", CommentForm())

        return context


class SubjectsList(ListBreadcrumbMixin, generic.ListView):
    """
    Display a list of all :model:`resources.Subject` objects.

    This view is used to browse available subjects/topics on StudyStack.

    **Context**
    ``subject_list``
        List of :model:`resources.Subject` objects (explicitly named by
        ``context_object_name``).



    **Template**
    :template:`resources/subject_list.html`
    """

    model = Subject
    template_name = "resources/subject_list.html"
    context_object_name = "subject_list"

    def get_queryset(self, **kwargs):
        """
        Retrieve the queryset of subjects to display.

        Currently returns all subjects using the default model manager.
        This hook is available for future extension, for example ordering by
        name or filtering to subjects that have published resources.

        Args:
            **kwargs: URL keyword arguments captured by the route.

        Returns:
            QuerySet: All :model:`resources.Subject` objects.
        """
        subject_list = super().get_queryset()
        return subject_list


class SubjetResourceListView(
    ListBreadcrumbMixin,
    generic.ListView,
):
    """
    Display a list of published resources for a specific subject.

    The subject is resolved from the URL slug, and only published resources
    linked to that subject are displayed.

    **Context**
    ``resources``
        List of :model:`resources.Resource` objects for the selected subject.

    ``subject``
        The :model:`resources.Subject` instance resolved from the URL.

    ``page_obj``
        Pagination object for the current page (if pagination is added).

    **Template**
    :template:`resources/subject_resource_list.html`
    """

    model = Resource
    template_name = "resources/subject_resource_list.html"
    context_object_name = "resources"

    @property
    def crumbs(self):
        """
        Provide breadcrumb entries for the current subject page.

        Overrides the default breadcrumb label so that the breadcrumb displays
        the subject name instead of a generic model label.

        Returns:
            list[tuple[str, str]]: Breadcrumb items as (label, url) tuples.
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
        """
        Retrieve published resources associated with the current subject.

        This method resolves the subject from the URL slug, then filters
        :model:`resources.Resource` objects where that subject is linked via
        the many-to-many relationship.

        Query optimisation:
        - ``select_related("author")`` reduces queries when rendering author data
        - ``prefetch_related("subjects")`` reduces queries when rendering subjects

        Returns:
            QuerySet: Published resources linked to the resolved subject.
        """
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
        """
        Add the current subject to the template context.

        This enables the template to display subject metadata (such as
        the subject name) alongside the list of resources.

        Args:
            **kwargs: Additional context provided by Django.

        Returns:
            dict[str, Any]: Context dictionary passed to the template.
        """
        context = super().get_context_data(**kwargs)
        context["subject"] = self.subject
        return context
