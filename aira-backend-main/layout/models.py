from django.db import models
from core.models import Project
from tools.models import ToolInstance


class Node(models.Model):
    NODE_TYPE_CHOICES = [
        ('1way', '1 Way'),
        ('2way', '2 Way'),
        ('3way', '3 Way'),
    ]
    # super nodes
    entry_node = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    node_type = models.CharField(
        max_length=5, choices=NODE_TYPE_CHOICES, default='1way')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True, default='')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='nodes',null=True)

    layout_data = models.JSONField(default=dict, blank=True)

    # for tools
    tool_instance = models.ForeignKey(
        ToolInstance, null=True, blank=True, on_delete=models.SET_NULL)

    # for agents
    role_prompt = models.TextField(blank=True)
    personality_prompt = models.TextField(blank=True)
    instructions_prompt = models.TextField(blank=True)
    goal_prompt = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_connected_agents_prompt(self):
        prompt = "You have the following agents:\n"
        edges = Edge.objects.filter(source=self).exclude(
            target__node_type='1way').order_by('target__pk')
        for edge in edges:
            prompt += edge.target.name+": "+edge.target.description+"\n"

        edges = Edge.objects.filter(source=self).filter(target__node_type='1way').exclude(target__entry_node=None).all()
        for edge in edges:
            prompt += edge.target.name+": "+edge.target.description+"\n"
        return prompt

    def get_connected_tools_prompt(self):
        prompt = "You have following tools and the corresponding commands:\n\n"
        edges = Edge.objects.filter(source=self).filter(
            target__node_type='1way').exclude(target__tool_instance=None).order_by('target__pk')
        for edge in edges:
            prompt += edge.target.name+": "+"\n"
            prompt += "Abilities:"+"\n"
            prompt += edge.target.tool_instance.tool.abilities+"\n"
            prompt += "Commands formats for abilities:"+"\n"
            prompt += edge.target.tool_instance.tool.input_format+"\n\n\n\n"
        return prompt

    def get_full_prompt(self):
        prompt = "Your an intelligent AI agent orchestrating other AI agents and tools." + '\n'
        prompt += self.role_prompt + '\n\n'
        prompt += self.personality_prompt + '\n\n'
        prompt += self.instructions_prompt + '\n\n'
        prompt += self.goal_prompt + '\n\n'
        prompt += self.get_connected_agents_prompt() + '\n\n'
        prompt += self.get_connected_tools_prompt() + '\n\n'
        prompt += """You communicate with the user and other agents through messages.
The format of messages to communicate with agents and user is:
{'to' : 'user' or '<agent name>' ,
   'msg': <message to user or agent or tool>,
}

The format of messages to communicate with tools is:
{'to' : '<tool>' ,
   'msg': <valid command>,
}

generate messages in json format.
You can only communicate in messages in json format."""
        return prompt


class Edge(models.Model):
    source = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='source_edges')
    source_handle = models.CharField(default=None, max_length=128, null=True)
    target = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='target_edges')
    target_handle = models.CharField(default=None, max_length=128, null=True)
    identifier = models.CharField(default=None, max_length=128)

    def __str__(self):
        return f"{self.source} -> {self.target} ({self.identifier})"
