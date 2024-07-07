from django.urls import path
from tools.views import get_all_tools, save_tool_config, get_tool_config

urlpatterns = [
    path('tools/', get_all_tools, name='get_all_tools'),
    path('tools/save-config/', save_tool_config, name='save_tool_config'),
    path('tools/get-config/', get_tool_config, name='get_tool_config'),
]
