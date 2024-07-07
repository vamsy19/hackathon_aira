from rest_framework import serializers
from .models import *
from tools.serializers import ToolInstanceSerializer


class NodeSerializer(serializers.ModelSerializer):
    tool_instance = ToolInstanceSerializer()

    class Meta:
        model = Node
        fields = '__all__'


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'


class NodeSerializerCreation(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'
