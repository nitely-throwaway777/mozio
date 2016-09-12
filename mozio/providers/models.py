# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from phonenumber_field.modelfields import PhoneNumberField
import pycountry

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models as gis_models
from django.utils.encoding import python_2_unicode_compatible


__all__ = [
    'Providers',
    'ServiceAreas']


LANGUAGES = [
    (lang.iso639_3_code, lang.name)
    for lang in sorted(pycountry.languages, key=lambda x: x.name)]

CURRENCIES = [
    (cur.letter, cur.name)
    for cur in sorted(pycountry.currencies, key=lambda x: x.name)]


@python_2_unicode_compatible
class Providers(models.Model):
    """
    Transportation supplier
    """

    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email address'), max_length=254)  # RFCs 3696
    phone_number = PhoneNumberField(_('phone number'),
                                    help_text=_('E164 format, e.g. "+41446681800"'))  # E.164 standard
    language = models.CharField(_('language'), max_length=3, choices=LANGUAGES)  # ISO 639
    currency = models.CharField(_('currency'), max_length=3, choices=CURRENCIES)  # ISO 4217

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ServiceAreas(models.Model):
    """
    Service Areas for Providers
    """

    provider = models.ForeignKey(Providers, related_name='service_areas')

    name = models.CharField(_('name'), max_length=255)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    polygons = gis_models.MultiPolygonField(_('polygons'), spatial_index=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.provider)
