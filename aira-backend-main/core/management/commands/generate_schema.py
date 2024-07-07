from django.core.management.base import BaseCommand
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
from drf_yasg.renderers import SwaggerJSONRenderer, SwaggerYAMLRenderer
from rest_framework import permissions
from django.conf import settings


class Command(BaseCommand):
    help = 'Generates API schema in JSON or YAML format'

    def add_arguments(self, parser):
        parser.add_argument('format', type=str, choices=['json', 'yaml'])

    def handle(self, *args, **options):
        format = options['format']
        generator = OpenAPISchemaGenerator(
            info=openapi.Info(
                title="API Documentation",
                default_version='v1',
                description="API documentation for the Naulets app/web-app",
            ),
        )
        schema = generator.get_schema(request=None, public=True)

        if format == 'json':
            renderer = SwaggerJSONRenderer()
            content = renderer.render(schema)
            for filepath in settings.SCHEMA_FILE_PATHS:
                with open(filepath+".json", 'wb') as file:
                    file.write(content)
            self.stdout.write(self.style.SUCCESS(
                'Successfully generated JSON schema files'))

        elif format == 'yaml':
            renderer = SwaggerYAMLRenderer()
            content = renderer.render(schema)
            with open(settings.SCHEMA_FILE_PATH+'.yaml', 'wb') as file:
                file.write(content)
            self.stdout.write(self.style.SUCCESS(
                'Successfully generated YAML schema'))
