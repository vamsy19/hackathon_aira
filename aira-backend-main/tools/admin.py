from django.contrib import admin
from .models import Tool, ToolInstance


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'abilities', 'input_format', 'output_format')
    search_fields = ('name', 'abilities')
    list_filter = ('name',)


@admin.register(ToolInstance)
class ToolInstanceAdmin(admin.ModelAdmin):
    list_display = ('tool', 'config')
    search_fields = ('tool__name',)
    list_filter = ('tool',)
