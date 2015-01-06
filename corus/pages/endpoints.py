#!/usr/bin/env python


"""
"""

from corus.common.args import html
import nudge.arg as args
from nudge.publisher import Endpoint, Args
from nudge.renderer import Redirect


endpoints = [
    Endpoint(
        name='View all pages',
        method='GET',
        uri='/cor/console/pages/?$',
        function='pages.view_pages_endpoint',
        args=Args(
            delete=args.String('del', optional=True),
            new=args.String('new', optional=True),
        ),
        renderer=html),

    Endpoint(
        name='Create new page',
        method='POST',
        uri='/cor/console/pages/new/?$',
        function='pages.new_page_endpoint',
        args=Args(
            # Page props
            path=args.String('path'),
            base_template=args.String('base_template'),

            # Version Props
            title=args.String('title'),
            content=args.String('content'),
            notes=args.String('notes', optional=True),
        ),
        renderer=Redirect()
    ),

    Endpoint(
        name='Create new version',
        method='POST',
        uri='/cor/console/pages/version/?$',
        function='pages.new_version_endpoint',
        args=Args(
            # Page props
            path=args.String('path'),
            base_template=args.String('base_template'),

            # Version Props
            title=args.String('title'),
            content=args.String('content'),
            revision_notes=args.String('revision_notes', optional=True),
            publish=args.Boolean('publish'),
        ),
        renderer=Redirect()
    ),

    Endpoint(
        name='Edit a page',
        method='GET',
        uri='/cor/console/pages/edit/?$',
        function='pages.edit_page_endpoint',
        args=Args(
            path=args.String('path', optional=True),
            delete=args.String('del', optional=True),
            new=args.String('new', optional=True),
        ),
        renderer=html),

    # *WARNING* this endpoint needs to be loaded LAST as it will match all
    Endpoint(
        name='Serve Page',
        method='GET',
        uri='/(?P<path>.*)$',
        function='pages.serve_endpoint',
        args=Args(
            path=args.String('path', optional=True),
            version=args.String('version', optional=True),
        ),
        renderer=html),

    # Endpoint(
    #     name='View the edit page',
    #     method='GET',
    #     uri='/cor/console/pages/edit/?$',
    #     function='pages.view_edit_page_endpoint',
    #     args=Args(
    #         path=args.String('path'),
    #     ),
    #     renderer=html
    # ),
    # Endpoint(
    #     name='Delete a page',
    #     method='GET',
    #     uri='/cor/console/pages/delete/?$',
    #     function='pages.delete_page_endpoint',
    #     args=Args(
    #         path=args.String('path'),
    #     ),
    #     renderer=Redirect()
    # ),
    # Endpoint(
    #     name='Save a page',
    #     method='POST',
    #     uri='/cor/console/pages/save/?$',
    #     function='pages.save_page_endpoint',
    #     args=Args(
    #         path=args.String('path'),
    #         title=args.String('title'),
    #         content=args.String('content', optional=True),
    #         notes=args.String('notes', optional=True),
    #         active=args.Boolean('active', optional=True),
    #     ),
    #     renderer=Redirect()
    # ),
]