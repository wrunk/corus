#!/usr/bin/env python


from google.appengine.api.images import get_serving_url, delete_serving_url
from google.appengine.ext import blobstore, ndb
import logging
from nudge.engine import EngineService
from nudge.error import HTTPError


_log = logging.getLogger(__name__)


# TODO test using gifs, pngs, and non image files on the server
class CorusFile(ndb.Model):
    '''
    ID: uploaded file's name as it existed on their computer.

    Right now this uses blobstore to store the files. Using GCS would probably be better, but that
    requires using Google's horrible cloud console to connect GCS to app engine, etc.
    '''

    # CDN serving URL. Support dynamic resizing by specifying =s5000 where 5000 is the greatest
    # dimension in pixels
    serving_url = ndb.StringProperty(indexed=False, required=True)
    # Blob props provided by Google's BlobInfo object
    blob_content_type = ndb.StringProperty(indexed=False, required=True)
    blob_creation = ndb.DateTimeProperty(required=True, indexed=True)
    blob_key = ndb.BlobKeyProperty(indexed=False, required=True)
    blob_md5_hash = ndb.StringProperty(indexed=False, required=True)
    blob_size_in_bytes = ndb.IntegerProperty(indexed=False, required=True)


class FileService(EngineService):
    endpoint_methods = ['view_files_endpoint', 'delete_file_endpoint', 'view_file_endpoint']
    published_members = ['upload_complete']
    name = 'file'

    class FileAlreadyExistsError(HTTPError):
        message = "File already exists, can't reupload"
        status_code = 400

    def view_files_endpoint(self, delete=None):
        upload_url = blobstore.create_upload_url('/upload')
        files = CorusFile.query().order(-CorusFile.blob_creation).fetch()
        if delete is not None:
            for i, f in enumerate(files):
                if f.key.id() == delete.lower():
                    del files[i]
        return {'template_name': 'console/files.html', 'upload_url': upload_url, 'files': files}

    def upload_complete(self, file_info):
        """
        Called by the webapp2 upload handler in main.py after a blob is uploaded.

        *Note* We should try to never throw a hard error here since we are not set up to handle it
        """
        f = CorusFile.get_by_id(file_info.filename.lower())
        if f:
            _log.warn("File already exists! (%s) cant re-upload", file_info.filename.lower())
            return ''
            # TODO Be able to use this properly
            # raise self.FileAlreadyExistsError()

        f = CorusFile(id=file_info.filename.lower())
        f.blob_key = file_info.key()
        # TODO this could fail if not an image. Make an endpoint to show files (pdfs etc).
        # f.url = get_serving_url(file_info.key(), size=1500)
        f.serving_url = get_serving_url(file_info.key())
        f.blob_content_type = file_info.content_type
        f.blob_creation = file_info.creation
        f.blob_md5_hash = file_info.md5_hash
        f.blob_size_in_bytes = file_info.size
        f.put()
        return f.key.id()

    def delete_file_endpoint(self, name):
        f = CorusFile.get_by_id(name)
        b = blobstore.BlobInfo(f.blob_key)
        if f.serving_url:
            delete_serving_url(b.key())
        b.delete()
        f.key.delete()
        return str('/cor/console/files/?del=' + name)

    def view_file_endpoint(self, name):
        """
        name can be None here for cases where the upload failed (like if they try to upload a dup)
        """
        f = None
        if name:
            f = CorusFile.get_by_id(name)
        return {'template_name': 'console/file_view.html', 'file': f}
