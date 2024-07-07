from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from tools.serializers import ToolSerializer, ToolInstanceSerializer

get_all_tools_schema = swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description='List of all tools retrieved successfully',
            schema=ToolSerializer(many=True)
        ),
        404: openapi.Response(description='Tools not found'),
    }
)

save_tool_config_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'node': openapi.Schema(type=openapi.TYPE_STRING, description='Node ID'),
            'tool': openapi.Schema(type=openapi.TYPE_STRING, description='Tool ID'),
            'config': openapi.Schema(type=openapi.TYPE_OBJECT, description='Tool configuration'),
        },
        required=['node', 'tool', 'config']
    ),
    responses={
        201: openapi.Response(description='Tool instance created successfully'),
        400: openapi.Response(description='Invalid input data'),
    }
)

get_tool_config_schema = swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('node_id', openapi.IN_PATH,
                          description="Node ID", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response(
            description='Tool configuration retrieved successfully',
            schema=ToolInstanceSerializer()
        ),
        404: openapi.Response(description='Node or Tool instance not found'),
    }
)
