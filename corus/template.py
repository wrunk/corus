#!/usr/bin/env python

#!/usr/bin/env python


"""
Provide a rich file template rendering service

"""
from jinja2 import Environment, FileSystemLoader
import logging
from nudge.engine import EngineService
import os


_log = logging.getLogger(__name__)


class TemplateService(EngineService):
    endpoint_methods = None
    published_members = ['render', 'get_base_templates', 'render_from_string', 'get_source']
    name = 'template'
    # Project's base path
    __base_path = os.path.dirname(os.path.realpath(__file__))
    # User's application base path
    __app_base_path = None
    __app_base_templates_dir = None
    # Our internal jinja2 template env
    __template_env = None
    __fs_loader = None

    def __init__(self, engine):

        super(TemplateService, self).__init__(engine)

        self.__app_base_path = self.engine.get('csettings', 'all')()['templates_root']
        self.__app_base_templates_dir = self.engine.get('csettings', 'all')()['base_templates_dir']

        self.__fs_loader = FileSystemLoader(
            # Search path gets saved as a list in jinja2 internally, so we could
            # add to it if necessary.
            searchpath=[self.__base_path + '/templates', self.__app_base_path],
            encoding='utf-8',
        )
        self.__template_env = Environment(loader=self.__fs_loader, trim_blocks=True)

    def render(self, template_name, context):
        """
        Context must be a dictionary right now, but could also be **kwargs
        """
        # Add the global corus settings from engine to the context
        context['csettings'] = self.engine.get('csettings', 'all')()
        return self.__template_env.get_template(template_name).render(context)

    def render_from_string(self, s, context):
        # TODO we should probably make a new loader for getting stuff out of NDB
        return self.__template_env.from_string(s).render(context)

    def get_base_templates(self):
        # The call to FS loader list_templates is a sorted set, so just append, return
        bts = []
        for t in self.__fs_loader.list_templates():
            if t.startswith(self.__app_base_templates_dir):
                bts.append(t)
        return bts

    def get_source(self, template_name):
        source, filename, uptodate = self.__fs_loader.get_source(self.__template_env, template_name)
        return source
