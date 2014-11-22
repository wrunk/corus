#!/usr/bin/env python
# Copyright 2013 DeadHeap.com


"""
Endpoints for the email section of the console
"""
from nudge.publisher import Endpoint, Args
import nudge.arg as args
from nudge.publisher import Endpoint
from nudge.renderer import HTML, Redirect, Plain, Result


# How do we get the nudge renderers and such to have access to the console?
_engine = None
def set_engine(engine):
    global _engine
    _engine = engine


def html(content):
    if isinstance(content, dict):
        content = _engine.get('template', 'render')(content['template_name'], content)
    return Result(content=content, content_type='text/html; charset=utf-8', http_status=200)

endpoints = [
    Endpoint(
        name='View files',
        method='GET',
        uri='/cor/console/files/?$',
        function='file.view_files_endpoint',
        args=Args(
            delete=args.String('del', optional=True),
        ),
        renderer=html),
    # TODO it would be better to use method DELETE or POST
    Endpoint(
        name='Delete a File',
        method='GET',
        uri='/cor/console/files/del/?$',
        function='file.delete_file_endpoint',
        args=Args(
            name=args.String('name'),
        ),
        renderer=Redirect()
    ),
    Endpoint(
        name='Edit a file and view',
        method='GET',
        uri='/cor/console/files/view?$',
        function='file.view_file_endpoint',
        args=Args(
            name=args.String('name', optional=True),
        ),
        renderer=html),
]