from django.urls import path
from .views import *

urlpatterns = [
    path('nodes/create/', create_node, name='create_node'),
    path('nodes/update/<str:node_id>/', update_node, name='update_node'),
    path('layout/update/', update_layout, name='update_layout'),
    path('layout/<str:project_id>/', get_layout, name='get_layout'),
    path('nodes/run/', run_node, name='run_node'),
    path('nodes/super/create/', create_super_node, name='create_super_node'),
    path('nodes/super/', get_all_super_nodes, name='get_all_super_nodes'),
]
