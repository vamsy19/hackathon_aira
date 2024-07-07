from rest_framework import serializers
from tools.models import Tool, ToolInstance


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'abilities',
                  'config', 'input_format', 'output_format']


class ToolInstanceSerializer(serializers.ModelSerializer):
    tool = ToolSerializer()

    class Meta:
        model = ToolInstance
        fields = ['id', 'tool', 'config']
