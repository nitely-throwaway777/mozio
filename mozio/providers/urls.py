# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter

from .views import ProvidersViewSet, ServiceAreasViewSet


router = DefaultRouter(schema_title='API')
router.register(r'providers', ProvidersViewSet, base_name='providers')
router.register(r'service-areas', ServiceAreasViewSet, base_name='service-areas')
urlpatterns = router.urls
