from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import NodeSerializer

create_node_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'node_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the node', enum=['1way', '2way', '3way']),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the node'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the node'),
            'project': openapi.Schema(type=openapi.TYPE_STRING, description='Project ID'),
        },
        required=['node_type', 'name', 'project'],
    ),
    responses={
        201: openapi.Response(description='Node created successfully'),
        400: openapi.Response(description='Invalid input'),
    }
)


update_layout_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'project': openapi.Schema(type=openapi.TYPE_STRING, description='Project ID'),
            'nodes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='Node ID'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Node Name'),
                    # Add other node properties here
                }),
                description='List of nodes'
            ),
            'edges': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                    'source': openapi.Schema(type=openapi.TYPE_STRING, description='Source Node ID'),
                    'target': openapi.Schema(type=openapi.TYPE_STRING, description='Target Node ID'),
                    # Add other edge properties here
                }),
                description='List of edges'
            ),
        },
        required=['project', 'nodes', 'edges'],
    ),
    responses={
        200: openapi.Response(description='Layout updated successfully'),
        400: openapi.Response(description='Invalid input'),
    }
)

get_layout_schema = swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'project_id',
            openapi.IN_PATH,
            description="ID of the project",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Layout retrieved successfully',
            examples={
                'application/json': {
                    'nodes': [
                        {
                            'id': 'string',
                            'name': 'string',
                            'node_type': 'string',
                            'description': 'string',
                            'project': 'string',
                            'layout_data': {}
                        }
                    ],
                    'edges': [
                        {
                            'source': 'string',
                            'source_handle': 'string',
                            'target': 'string',
                            'target_handle': 'string',
                            'identifier': 'string'
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(description='Project not found'),
    }
)


update_node_schema = swagger_auto_schema(
    method='patch',
    request_body=NodeSerializer,
    responses={
        200: openapi.Response(
            description='Node updated successfully',
            examples={
                'application/json': {
                    'id': 'string',
                    'name': 'string',
                    'node_type': 'string',
                    'description': 'string',
                    'project': 'string',
                    'layout_data': {}
                }
            }
        ),
        400: openapi.Response(description='Invalid input'),
        404: openapi.Response(description='Node not found'),
    }
)


run_node_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message to be processed by the node'),
            'node': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the node to run')
        },
        required=['node']
    ),
    responses={
        200: openapi.Response(
            description='Node run successfully',
            examples={
                'application/json': {
                    'message': 'Node run successfully',
                    'input_message': 'string',
                    'node': 'string'
                }
            }
        ),
        400: openapi.Response(description='Invalid input'),
        404: openapi.Response(description='Node not found'),
    }
)

run_node_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Message to be processed by the node'),
            'node': openapi.Schema(type=openapi.TYPE_OBJECT, description='Node data', properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the node')
            }, required=['id'])
        },
        required=['msg', 'node']
    ),
    responses={
        200: openapi.Response(
            description='Node run successfully',
            examples={
                'application/json': {
                    'message': 'Node run successfully',
                    'input_message': 'string',
                    'node': 'string'
                }
            }
        ),
        400: openapi.Response(description='Invalid input'),
        404: openapi.Response(description='Node not found'),
    }
)


create_super_node_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'entry_node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the entry node'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the super node'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the super node')
        },
        required=['entry_node_id', 'name']
    ),
    responses={
        201: openapi.Response(
            description='Super node created successfully',
            examples={
                'application/json': {
                    'message': 'Super node created successfully',
                    'super_node_id': 'integer'
                }
            }
        ),
        400: openapi.Response(description='Invalid input'),
        404: openapi.Response(description='Entry node not found'),
    }
)

get_all_super_nodes_schema = swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description='List of all super nodes',
            examples={
                'application/json': [
                    {
                        'id': 'integer',
                        'name': 'string',
                        'description': 'string',
                        'entry_node': 'integer',
                        'project': 'integer',
                        'node_type': 'string'
                    }
                ]
            }
        ),
        404: openapi.Response(description='No super nodes found'),
    }
)
