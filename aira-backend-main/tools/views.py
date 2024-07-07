from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tools.serializers import ToolSerializer
from tools.models import Tool, ToolInstance
from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from layout.models import Node
from .models import Tool
from layout.serializers import NodeSerializer


@get_all_tools_schema
@api_view(['GET'])
def get_all_tools(request):
    tools = Tool.objects.all()
    serializer = ToolSerializer(tools, many=True)
    return Response(serializer.data)


@save_tool_config_schema
@api_view(['POST'])
def save_tool_config(request):
    # print(request.data)
    try:
        node = Node.objects.get(id=request.data['node'])
        tool = Tool.objects.get(id=request.data['tool'])
        config = request.data.get('config')

        if not config:
            return Response({'error': 'Invalid input data'}, status=400)

        tool_instance = ToolInstance.objects.create(tool=tool, config=config)
        node.tool_instance = tool_instance
        node.save()

        node_serializer = NodeSerializer(node)
        return Response(node_serializer.data, status=201)
    except Node.DoesNotExist:
        return Response({'error': 'Node not found'}, status=404)
    except Tool.DoesNotExist:
        return Response({'error': 'Tool not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@get_tool_config_schema
@api_view(['GET'])
def get_tool_config(request, node_id):
    try:
        node = Node.objects.get(id=node_id)
        tool_instance = node.tool_instance
        serializer = ToolInstanceSerializer(tool_instance)
        return Response(serializer.data, status=200)
    except Node.DoesNotExist:
        return Response({'error': 'Node not found'}, status=404)
    except ToolInstance.DoesNotExist:
        return Response({'error': 'Tool instance not found'}, status=404)
