from .tasks import Orchestra
import json
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Node
from .serializers import NodeSerializer, EdgeSerializer, NodeSerializerCreation
from .schemas import *
from .models import Edge
from core.models import Project

@create_node_schema
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_node(request):
    serializer = NodeSerializerCreation(data=request.data)
    if serializer.is_valid():
        node = serializer.save()
        print(f"Entry point of new node: {node.entry_node}")
        if node.entry_node:
            connected_nodes = []
            def get_connected_nodes(node):
                edges = Edge.objects.filter(source=node)
                for edge in edges:
                    if edge.target not in connected_nodes:
                        connected_nodes.append(edge.target)
                        get_connected_nodes(edge.target)
            get_connected_nodes(node.entry_node)
            print("Connected nodes:", [n.name for n in connected_nodes])
            for node in connected_nodes:
                node.id = None
                node.project = None
                node.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@update_node_schema
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_node(request, node_id):
    try:
        node = Node.objects.get(id=node_id)
    except Node.DoesNotExist:
        return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = NodeSerializer(node, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@get_layout_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_layout(request, project_id):
    try:
        nodes = Node.objects.filter(project__id=project_id)
        edges = Edge.objects.filter(
            source__project__id=project_id, target__project__id=project_id)

        node_list = NodeSerializer(nodes, many=True).data
        edge_list = EdgeSerializer(edges, many=True).data

        layout = {
            'nodes': node_list,
            'edges': edge_list
        }

        return Response(layout, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


@update_layout_schema
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_layout(request):
    data = request.data
    # print(data)  # Print the data for debugging purposes
    project = data.get('project')
    nodes = data.get('nodes')
    edges = data.get('edges')

    # update edges
    existing_edges = Edge.objects.filter(
        source__project__id=project, target__project__id=project)
    existing_edge_ids = set(
        existing_edges.values_list('identifier', flat=True))
    new_edge_ids = set(edge['id'] for edge in edges)

    # Delete edges not present in the new edges list
    edges_to_delete = existing_edges.exclude(identifier__in=new_edge_ids)
    edges_to_delete.delete()

    # Create new edges
    for edge in edges:
        if edge['id'] not in existing_edge_ids:
            source_node = Node.objects.get(
                id=int(edge['source']), project__id=project)
            target_node = Node.objects.get(
                id=int(edge['target']), project__id=project)
            Edge.objects.create(
                source=source_node,
                source_handle=edge['sourceHandle'],
                target=target_node,
                target_handle=edge['targetHandle'],
                identifier=edge['id']
            )

    # update nodes
    existing_nodes = Node.objects.filter(project__id=project)
    existing_node_ids = set(existing_nodes.values_list('id', flat=True))
    new_node_ids = set(node['data']['id'] for node in nodes)

    # Delete nodes not present in the new nodes list
    nodes_to_delete = existing_nodes.exclude(id__in=new_node_ids)
    nodes_to_delete.delete()

    # Updating nodes layout data
    for layout_node in nodes:
        node = Node.objects.get(id=layout_node['data']['id'])
        layout_data = layout_node
        del layout_data['data']
        node.layout_data = layout_data
        node.save()

    return Response({"message": "Layout updated successfully"}, status=status.HTTP_200_OK)


orchestras = []

@run_node_schema
@api_view(['POST'])
def run_node(request):

    msg = {}
    print(f"AFEAFEA: {request.data['msg']}")
    msg['data'] = request.data.get('msg')
    node_data = request.data.get('node')

    try:
        node = Node.objects.get(id=node_data["id"])
        msg['metadata'] = {"from": "user", "to": node.name}

        for orchestra in orchestras:
            if orchestra.entry_node == node:
                res = orchestra.run(msg)
                return Response(res, status=status.HTTP_200_OK)

        orchestra = Orchestra(node)
        orchestras.append(orchestra)
        res = orchestra.run(msg)
        return Response(res, status=status.HTTP_200_OK)

    except Node.DoesNotExist:
        return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@create_super_node_schema
@api_view(['POST'])
def create_super_node(request):
    entry_node_id = request.data.get('entry_node_id')
    name = request.data.get('name')
    description = request.data.get('description')

    if not entry_node_id or not name:
        return Response({"error": "entry_node_id and name are required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        entry_node = Node.objects.get(id=entry_node_id)
    except Node.DoesNotExist:
        return Response({"error": "Entry node not found"}, status=status.HTTP_404_NOT_FOUND)

    super_node = Node.objects.create(
        entry_node=entry_node,
        name=name,
        description=description,
        project=entry_node.project,
        node_type='1way'
    )

    return Response({"message": "Super node created successfully", "super_node_id": super_node.id}, status=status.HTTP_201_CREATED)

@get_all_super_nodes_schema
@api_view(['GET'])
def get_all_super_nodes(request):
    super_nodes = Node.objects.exclude(entry_node__isnull=True)
    serializer = NodeSerializer(super_nodes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
