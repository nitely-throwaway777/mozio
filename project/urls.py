# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

import mozio.urls


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    """
    API Docs
    """
    generator = schemas.SchemaGenerator(title='Mozio API')
    return response.Response(generator.get_schema(request=request))


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', schema_view),
    url(r'^', include(mozio.urls))
]
