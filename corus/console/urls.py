from django.views.generic.base import TemplateView
from django.conf.urls import patterns, url
from corus.console import views

urlpatterns = patterns('',
    url(r'^cor/console/?$', views.HomeHandler.as_view(), name='home'),
)