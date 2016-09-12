# -*- coding: utf-8 -*-

from django.conf.urls import url, include

import mozio.providers.urls


v1_patterns = [
    url(r'^', include(mozio.providers.urls, namespace='providers'))
]

version_patterns = [
    url(r'^v1/', include(v1_patterns, namespace='v1')),
]

urlpatterns = [
    url(r'^api/', include(version_patterns, namespace='api', app_name='mozio')),
]
