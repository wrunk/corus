#!/usr/bin/env python


from corus.common.args import html
from nudge.publisher import Endpoint, Args
import nudge.arg as args
from nudge.publisher import Endpoint
from nudge.renderer import HTML, Redirect, Plain, Result


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