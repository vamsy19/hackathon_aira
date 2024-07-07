from django.contrib import admin
from .models import LLM, Tool, Agent, Connection

admin.site.register(LLM)
admin.site.register(Tool)
admin.site.register(Agent)
admin.site.register(Connection)
