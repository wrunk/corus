#!/usr/bin/env python


"""
Corus main driver. Provides the primary nudge wsgi_app and a wa2_wsgi_app for use with file uploads
"""


from corus.console.endpoints import endpoints as console_endpoints
from corus.engine import engine
from corus.file.endpoints import endpoints as file_endpoints
from corus.pages.endpoints import endpoints as pages_endpoints
from google.appengine.ext.webapp import blobstore_handlers
import logging
from nudge.publisher import ServicePublisher
import webapp2


logging.getLogger().setLevel(logging.DEBUG)
_log = logging.getLogger(__name__)


# What is this? Nudge wsgi app, python http app
# TODO configure default error handler
wsgi_app = ServicePublisher(endpoints=console_endpoints + file_endpoints + pages_endpoints,
                            engine=engine)


# TODO see if theres a way to provide a better error page for repeated uploads on the same
# blobstore url key
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file_info')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        url = engine.get('file', 'upload_complete')(blob_info)
        self.redirect(str("/cor/console/files/view?name=" + url))


wa2_wsgi_app = webapp2.WSGIApplication([('/upload', UploadHandler),], debug=True)
