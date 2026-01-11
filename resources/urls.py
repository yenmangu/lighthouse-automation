from django.urls import path
from .views import (
    ResourceDetail,
    ResourceList,
    SubjectsList,
    SubjetResourceListView,
    CreateResource,
    ResourceDelete,
)

app_name = "resources"

urlpatterns = [
    path(
        "",
        ResourceList.as_view(),
        name=ResourceList.list_view_name,
    ),
    path(
        "resources/<slug:slug>/",
        ResourceDetail.as_view(),
        name=ResourceDetail.detail_view_name,
    ),
    path(
        "resources/<slug:slug>/delete/",
        ResourceDelete.as_view(),
        name=ResourceDelete.delete_view_name,
    ),
    path(
        "subjects/",
        SubjectsList.as_view(),
        name=SubjectsList.list_view_name,
    ),
    # path(
    #     "subjects/",
    #     views.<view>.as_view(),
    #     name="all_subjects",
    # ),
    path(
        "subjects/<slug:slug>/",
        SubjetResourceListView.as_view(),
        name="subject_resource_list",
    ),
    path(
        "create/",
        CreateResource.as_view(),
        name=CreateResource.create_view_name,
    ),
]
