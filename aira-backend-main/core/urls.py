from django.urls import path
from .views import organization_list_create, project_list_create

urlpatterns = [
    path('organizations/', organization_list_create,
         name='organization-list-create'),
    path('projects/', project_list_create, name='project-list-create'),
]
