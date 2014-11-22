#!/usr/bin/env python


from corus_settings import settings
from google.appengine.api.images import get_serving_url, delete_serving_url
from google.appengine.ext import blobstore, ndb
import logging
from nudge.engine import EngineService
from nudge.json import ObjDict
from nudge.error import HTTPError
import os


_log = logging.getLogger(__name__)


class SettingsService(EngineService):
    endpoint_methods = None
    published_members = ['all']
    name = 'csettings'
    __all_settings = None

    def __init__(self, engine):
        self.base_path = "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])

        with open(self.base_path + '/VERSION.txt') as fp:
            version = fp.read().strip()

        assert 5 <= len(version) <= 8 and '.' in version, 'Invalid corus version'

        _log.info("Setting corus version (%s) settings base path to (%s)", version, self.base_path)
        # Define our default corus settings here, the override from user's corus_settings.py
        self.__all_settings = ObjDict({
            'corus_version': version
        })
        for k, v in settings.items():
            self.__all_settings[k] = v

        super(SettingsService, self).__init__(engine)

    def all(self):
        """
        Return all the settings
        """
        return self.__all_settings

    def _load(self):
        pass

    def _load_version(self):
        pass