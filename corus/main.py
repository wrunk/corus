#!/usr/bin/env python


"""
Corus main driver. Provides the primary nudge wsgi_app and a wa2_wsgi_app for use with file uploads
"""
from corus.console.service import ConsoleService
from corus.console.endpoints import endpoints as console_endpoints
from corus.endpoints import endpoints
from corus.file.endpoints import endpoints as file_endpoints
from corus.file.endpoints import set_engine as set_file_engine
from corus.file.service import FileService
from corus.settings import SettingsService
from corus.template import TemplateService
from google.appengine.ext.webapp import blobstore_handlers
import logging
from nudge.publisher import ServicePublisher
from nudge.engine import Engine
import webapp2


logging.getLogger().setLevel(logging.DEBUG)
_log = logging.getLogger(__name__)


engine = Engine()
engine.register_service(ConsoleService)
engine.register_service(FileService)
engine.register_service(SettingsService)
engine.register_service(TemplateService)


# TODO figure out what to do in this case
set_file_engine(engine)


# What is this? Nudge wsgi app, python http app
# TODO configure default error handler
wsgi_app = ServicePublisher(endpoints=endpoints + console_endpoints + file_endpoints, engine=engine)


# TODO fix this
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file_info')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        url = engine.get('file', 'upload_complete')(blob_info)
        self.redirect(str("/cor/console/files/view?name=" + url))


wa2_wsgi_app = webapp2.WSGIApplication([('/upload', UploadHandler),], debug=True)
