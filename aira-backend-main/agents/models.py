from django.db import models
from core.models import Project


class LLM(models.Model):
    llm_model = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return self.llm_model


class Tool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    role = models.CharField(max_length=255)
    goal = models.TextField()
    backstory = models.TextField()
    llm = models.ForeignKey(LLM, on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='agents')
    tools = models.ManyToManyField(Tool, blank=True, related_name='agents')
    internal_agents = models.ManyToManyField(
        'self', blank=True, related_name='parent_agents', symmetrical=False)
    max_iter = models.IntegerField(default=25)
    max_rpm = models.IntegerField(null=True, blank=True)
    max_execution_time = models.IntegerField(null=True, blank=True)
    # verbose = models.BooleanField(default=False)
    # allow_delegation = models.BooleanField(default=True)
    # step_callback = models.TextField(null=True, blank=True)
    # cache = models.BooleanField(default=True)
    system_template = models.TextField(null=True, blank=True)
    prompt_template = models.TextField(null=True, blank=True)
    response_template = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.role


class Connection(models.Model):
    from_agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='outgoing_connections')
    to_agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='incoming_connections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_agent} -> {self.to_agent}"
