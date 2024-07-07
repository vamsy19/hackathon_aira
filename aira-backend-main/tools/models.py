from django.db import models
import importlib


class Tool(models.Model):
    name = models.CharField(max_length=255)
    abilities = models.TextField()
    config = models.JSONField(default=dict, blank=True)
    input_format = models.TextField()
    output_format = models.TextField()

    tool_class_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class ToolInstance(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    config = models.JSONField(default=dict, blank=True)

    data = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tool.name

    def get_tool_class(self):
        module_name, class_name = self.tool.tool_class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        tool_class = getattr(module, class_name)
        return tool_class

    def get_tool_instance(self):
        if self.data is None or "":
            return self.get_tool_class()(self.config)
        else:
            return self.get_tool_class().deserialize(self.data)

    def run(self, msg):
        t = self.get_tool_instance()
        output = t.on_input_received(msg)
        return output
