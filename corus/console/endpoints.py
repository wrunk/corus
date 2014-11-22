#!/usr/bin/env python
# Copyright 2013 DeadHeap.com

from nudge.publisher import Endpoint
from nudge.renderer import HTML

endpoints = [
    Endpoint(
        name='Get Console Homepage',
        method='GET',
        uri='/cor/console/?$',
        function='console.homepage_endpoint',
        # TODO make this take a context like django that will have a template prop
        renderer=HTML()
    ),
]
