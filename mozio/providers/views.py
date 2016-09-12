# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.contrib.gis.geos import Point

from .models import Providers, ServiceAreas
from .serializers import (
    ProvidersSerializer,
    ServiceAreasSerializer,
    PointSerializer)


__all__ = [
    'ProvidersViewSet',
    'ServiceAreasViewSet']


class ProvidersViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Providers
    """

    queryset = Providers.objects.order_by('name')
    serializer_class = ProvidersSerializer
    partial = True


class ServiceAreasViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ServiceAreas
    """

    queryset = ServiceAreas.objects.order_by('name')
    serializer_class = ServiceAreasSerializer
    partial = True

    @list_route()
    def find(self, request):
        """
        List of ServiceAreas containing a given Point

        URL params:
            lat: Point latitude
            long: Point longitude
        """
        point = PointSerializer(data=request.GET)
        point.is_valid(raise_exception=True)
        queryset = self.queryset.filter(
            polygons__intersects=Point(
                x=point.data['lat'],
                y=point.data['long']))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
