#!/usr/bin/env python
import sys
import logging

logging.getLogger().setLevel(logging.DEBUG)


from django.core.handlers import wsgi

app = wsgi.WSGIHandler()