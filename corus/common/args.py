#!/usr/bin/env python


from nudge.renderer import Result
from corus.engine import engine as _engine


def html(content):
    if isinstance(content, dict):
        content = _engine.get('template', 'render')(content['template_name'], content)
    return Result(content=content, content_type='text/html; charset=utf-8', http_status=200)