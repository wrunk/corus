#!/usr/bin/env python


import logging

from django.views.generic import TemplateView




_log = logging.getLogger(__name__)



class HomeHandler(TemplateView):
    template_name = "console/home.html"