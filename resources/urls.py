from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.ResourceList.as_view(),
        name="home",
    ),
    path(
        "resources/<slug:slug>/",
        views.ResourceDetail.as_view(),
        name="resource_detail",
    ),
    path(
        "subjects/<slug:slug>/",
        views.SubjetResourceListView.as_view(),
        name="subject_resource_list",
    ),
]
