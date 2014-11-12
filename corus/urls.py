from django.conf.urls import patterns, include, url

from django.contrib import sitemaps
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^', include('corus.console.urls')),
)