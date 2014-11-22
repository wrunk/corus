#!/usr/bin/env python

#!/usr/bin/env python


"""
Provide a rich file template rendering service

"""
import logging
from nudge.engine import EngineService
from jinja2 import Environment, FileSystemLoader

_log = logging.getLogger(__name__)
import os
print os.path.dirname(os.path.realpath(__file__))


class TemplateService(EngineService):
    endpoint_methods = None
    published_members = ['render']
    name = 'template'
    # Project's base path
    base_path = os.path.dirname(os.path.realpath(__file__))
    # Our internal jinja2 template env
    __template_env = None

    def __init__(self, engine):

        fs_loader = FileSystemLoader(
            # Search path gets saved as a list in jinja2 internally, so we could
            # add to it if necessary.
            searchpath=[self.base_path + '/templates'],
            encoding='utf-8',
        )
        self.__template_env = Environment(loader=fs_loader, trim_blocks=True)
        super(TemplateService, self).__init__(engine)

    def render(self, template_name, context):
        """
        Context must be a dictionary right now, but could also be **kwargs
        """
        # Add the global corus settings from engine to the context
        context['csettings'] = self.engine.get('csettings', 'all')()
        from pprint import pprint
        pprint(context['csettings'])
        return self.__template_env.get_template(template_name).render(context)
