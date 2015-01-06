#!/usr/bin/env python

"""
Create an engine to glue our services together. Nudge's engine protects access to non published
members
"""

from corus.console.service import ConsoleService
from corus.file.service import FileService
from corus.pages.service import PageService
from corus.settings import SettingsService
from corus.template import TemplateService
import logging
from nudge.engine import Engine


_log = logging.getLogger(__name__)


engine = Engine()
engine.register_service(ConsoleService)
engine.register_service(FileService)
engine.register_service(PageService)
engine.register_service(SettingsService)
engine.register_service(TemplateService)
