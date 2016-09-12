# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Polygon, MultiPolygon

from .models import Providers, ServiceAreas
from .serializers import ProvidersSerializer, ServiceAreasSerializer


class ProvidersViewSetTest(TestCase):
    """
    Should test all HTTP verbs
    """

    def setUp(self):
        self.provider_a = Providers.objects.create(
            name='foo',
            email='foo@bar.com',
            phone_number='+5491149461234',
            language='arg',
            currency='USD')

    def test_providers_list(self):
        """
        Should retrieve all providers
        """
        resp = self.client.get(reverse('api:v1:providers:providers-list'))
        self.assertEqual(
            dict(resp.data[0]),
            ProvidersSerializer(self.provider_a).data)

    def test_providers_create(self):
        """
        Should create a provider and return the serialized object
        """
        resp = self.client.post(
            reverse('api:v1:providers:providers-list'),
            data={
                'currency': 'USD',
                'email': 'foobar@bar.com',
                'language': 'arg',
                'name': 'bar',
                'phone_number': '+5491149461234'})
        self.assertEqual(
            resp.data,
            ProvidersSerializer(instance=Providers.objects.last()).data)

    def test_providers_destroy(self):
        """
        Should delete a provider
        """
        resp = self.client.delete(reverse(
            'api:v1:providers:providers-detail',
            kwargs={'pk': self.provider_a.pk}))
        self.assertIsNone(resp.data)
        self.assertEqual(list(Providers.objects.filter(pk=self.provider_a.pk)), [])

    def test_providers_partial_update(self):
        """
        Should let update a provider
        """
        resp = self.client.patch(
            reverse(
                'api:v1:providers:providers-detail',
                kwargs={'pk': self.provider_a.pk}),
            data=json.dumps({'name': 'bar'}),
            content_type="application/json")
        self.assertEqual(resp.data['name'], 'bar')

    def test_providers_retrieve(self):
        """
        Should get a provider
        """
        resp = self.client.get(reverse(
            'api:v1:providers:providers-detail',
            kwargs={'pk': self.provider_a.pk}))
        self.assertEqual(
            resp.data,
            ProvidersSerializer(self.provider_a).data)

    def test_providers_update(self):
        """
        Should update a provider
        """
        data = ProvidersSerializer(self.provider_a).data
        data['name'] = 'bar'
        resp = self.client.put(
            reverse(
                'api:v1:providers:providers-detail',
                kwargs={'pk': self.provider_a.pk}),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(resp.data, data)


class ServiceAreasViewSetTest(TestCase):
    """
    Should test all HTTP verbs
    """

    def setUp(self):
        self.provider_a = Providers.objects.create(
            name='foo',
            email='foo@bar.com',
            phone_number='+5491149461234',
            language='arg',
            currency='USD')
        self.service_area = ServiceAreas.objects.create(
            provider=self.provider_a,
            name='foo',
            price='10.00',
            polygons=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))))

    def test_service_areas_list(self):
        """
        Should retrieve all service areas
        """
        resp = self.client.get(reverse('api:v1:providers:service-areas-list'))
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)

    def test_service_areas_create(self):
        """
        Should create a service area and return the serialized object
        """
        resp = self.client.post(
            reverse('api:v1:providers:service-areas-list'),
            data=json.dumps({
                'provider': self.provider_a.pk,
                'name': 'bar',
                'price': '10.00',
                'polygons': {
                    'coordinates': [
                        [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.0, 0.0]]],
                        [[[1.0, 1.0], [1.0, 2.0], [1.0, 2.0], [1.0, 1.0]]]],
                    'type': 'MultiPolygon'}}),
            content_type="application/json")
        self.assertEqual(
            resp.data,
            ServiceAreasSerializer(instance=ServiceAreas.objects.last()).data)

    def test_service_areas_find(self):
        """
        Should find an area by lat & long params
        """
        resp = self.client.get(
            reverse('api:v1:providers:service-areas-find'),
            data={'lat': 0, 'long': 0.5})
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)
        self.assertEqual(
            len(resp.data['features']),
            1)

    def test_service_areas_find_many(self):
        """
        Should find an area by lat & long params
        """
        service_area_b = ServiceAreas.objects.create(
            provider=self.provider_a,
            name='zaz',
            price='20.00',
            polygons=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))))

        resp = self.client.get(
            reverse('api:v1:providers:service-areas-find'),
            data={'lat': 0, 'long': 0.5})
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)
        self.assertEqual(
            dict(resp.data['features'][1]),
            ServiceAreasSerializer(service_area_b).data)
        self.assertEqual(
            len(resp.data['features']),
            2)
