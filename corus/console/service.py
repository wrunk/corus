#!/usr/bin/env python


"""

"""
import logging
from nudge.engine import EngineService

_log = logging.getLogger(__name__)


class ConsoleService(EngineService):
    endpoint_methods = ['homepage_endpoint']
    published_members = None
    name = 'console'

    def homepage_endpoint(self):
        'Prepare the home page'
        return self.engine.get('template', 'render')('console/home.html', {})

