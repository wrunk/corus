#!/usr/bin/env python


from google.appengine.ext import ndb
import logging
from nudge.engine import EngineService
from nudge.error import HTTPError
from pprint import pformat
import random
import re
import urllib


_log = logging.getLogger(__name__)


class CorusPageIndex(ndb.Model):
    """
    ID: actual page path like "content/about-us" *without* a version #

    Need to write this model and the new CorusPageVersion in a txn
    """
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    # Needs to start at one.
    number_of_versions = ndb.IntegerProperty(default=1, indexed=False)

    # The current published/active versions of this page. One will be randomly chosen from this list
    # to serve each request
    # Version 1 automatically gets published by default
    published_versions = ndb.IntegerProperty(repeated=True, indexed=False)

    # Tags like homepage or profile or something to help find pages.
    # TODO consider moving this to search section
    # tags = ndb.StringProperty(repeated=True)

    # If this is false and a user tries to hit it, it will 404 (unless they are logged in as admin?)
    # This cannot change once selected. Must delete page.??
    # TODO how to handle this?
    is_active = ndb.BooleanProperty(indexed=False, default=True)

    # Note if this page is a base template so we can show all templates
    # ?Can base templates be served?
    is_base_template = ndb.BooleanProperty(indexed=True, required=True)

    # Private notes about this page
    private_notes = ndb.TextProperty(indexed=False, default='')


class CorusPageVersion(ndb.Model):
    '''
    ID: path like "content/about-us:<version#>"
    We will strip left and right spaces and slashes
    '''
    created = ndb.DateTimeProperty(auto_now_add=True)
    # Can't update a version

    # ?Perhaps just used for the actual html:head:title?
    title = ndb.StringProperty(indexed=False, required=True)
    content = ndb.TextProperty(indexed=False, required=True)

    # parent template. Will need to use a custom loader if it doesn't end with .html to pull from
    # datastore
    # UI Note, show a list of available base templates useable from file sys and queried base
    # templates
    # This needs to stay with the versions since changing it will GREATLY fuck things up if it
    # were part of the index
    base_template = ndb.StringProperty(indexed=True)

    # Private notes about this revision
    private_revision_notes = ndb.TextProperty(indexed=False, default='')


class PageService(EngineService):
    endpoint_methods = ['view_pages_endpoint', 'new_page_endpoint', 'serve_endpoint',
                        'edit_page_endpoint', 'new_version_endpoint']
    published_members = []
    name = 'pages'

    class PageNotFoundError(HTTPError):
        message = 'Page Not Found'
        status_code = 404

    # -----------------------------------------------
    # Front-end Serving Endpoints
    # -----------------------------------------------
    def serve_endpoint(self, path='home', version=None, context=None):
        # TODO allow servage of inactive pages if logged in as admin
        # TODO strip off the prefixed path from settings
        # TODO allow a way to force render from DB or DISK
        path = PageService._sanitize_path(path)
        page_idx = CorusPageIndex.get_by_id(path)
        if not page_idx:
            raise self.PageNotFoundError()
        if version:
            page = CorusPageVersion.get_by_id(path + ':' + version)
        else:
            page = CorusPageVersion.get_by_id(
                "%s:%s" % (path, random.choice(page_idx.published_versions)))

        if page.base_template and page.base_template not in ('base', 'full_page'):
            content = '{% extends "' + page.base_template + '" %}\n' + page.content
        else:
            content = page.content
        return self.engine.get('template', 'render_from_string')(content, {})

    # -----------------------------------------------
    # Console Facing Endpoints
    # -----------------------------------------------
    # TODO perhaps this is pages home and we have page versions or just the page edit
    # page then we have version create page since they cant be edited
    def view_pages_endpoint(self, delete=None, new=None):
        if delete and delete == new:
            raise ValueError('Delete cannot equal new')
        # TODO combine this with the _get_base_templates call
        pages = CorusPageIndex.query().order(-CorusPageIndex.updated).fetch()
        # found_new = False
        # if not new:
        #     found_new = True
        # # Remove any pages that were just deleted that might still show up in a query due to
        # # eventual consistency
        # for i, page in enumerate(pages):
        #
        #     if delete and page.key.id() == delete:
        #         del pages[i]
        #     elif not found_new and page.key.id() == new:
        #         found_new = True
        #
        # # We didn't find the most recently created page due to eventual consistency, add it to
        # # the page list
        # if not found_new:
        #     new_page = CorusPageIndex.get_by_id(new)
        #     pages.insert(0, new_page)

        return {
            'template_name': 'console/pages.html',
            'pages': pages,
            'base_templates': self._get_base_templates(check_files=True),
        }

    def edit_page_endpoint(self, path, delete=None, new=None):
        """
        Use get_multi to get all versions with strong consistency
        """
        page = CorusPageIndex.get_by_id(path)
        # I apologize this is just nasty. Perhaps if this is > 200 we grab the published versions,
        # put them on top, then grab the latest 100~200
        versions = ndb.get_multi([ndb.Key(CorusPageVersion, path + ":%i" % i) for i in range(
            1, page.number_of_versions + 1)])
        _log.info(pformat(versions))
        for v in versions:
            v._version = PageService._get_version_from_id(v.key.id())
        return {
            'template_name': 'console/page_edit.html',
            'page': page,
            'versions': versions,
            'latest_version': versions[-1],
            'base_templates': self._get_base_templates(check_files=True),
        }

    @staticmethod
    def _sanitize_path(path):
        if not re.match(r'[\w\-\.~/]{1,300}', path):
            raise ValueError("Path contains illegal characters")
        return path.lower().strip().strip('/')

    @staticmethod
    def _get_version_from_id(page_version_id):
        return int(page_version_id.split(':')[-1])

    @ndb.transactional(xg=True)
    def _put_page(self, page_index, page_version):
        fut = page_index.put_async()
        page_version.put()
        fut.get_result()

    def _create_new_page(self, path, base_template, title, content, notes):
        """
        This will clobber. Do error checking before here
        """
        idx = CorusPageIndex(id=path,
                             published_versions=[1],
                             is_base_template=base_template == 'base',
                             # TODO add this. should be like _base/default
                             private_notes=notes.strip())

        version = CorusPageVersion(id=path + ':1',
                                   title=title.strip(),
                                   content=content.strip(),
                                   base_template=base_template.strip(),
                                   private_revision_notes='First version!')
        self._put_page(idx, version)
        return idx, version

    def _get_base_templates(self, check_files=False):
        """
        Get all possible base templates in a sorted LoL with (machine_name, 'Title')
        Full page
        :return:
        """
        base_templates = {
            'base': 'Base Template (Advanced - Make a New Theme)',
            'full_page': 'Full Page (Need to provide the full HTML for the page) (No base template)'
        }
        if check_files:
            # This will give us back a list of relative path base templates like base/base.html
            file_names = self.engine.get('template', 'get_base_templates')()
            idx_futures = {}
            # Try to get all the datastore objects for our base templates async and create them
            # if they DNE
            for f in file_names:
                idx_futures[f] = CorusPageIndex.get_by_id_async(f)
            for tname, fut in idx_futures.items():
                template = fut.get_result()
                if not template:
                    source = self.engine.get('template', 'get_source')(tname)
                    _log.warn("Creating new base template (%s)", tname)
                    idx, version = self._create_new_page(
                        path=tname,
                        base_template='base',
                        title='%s auto created from file' % tname,
                        content=source,
                        notes='This base template was auto created.'
                    )
                    base_templates[tname] = version.title

        _bases = CorusPageIndex.query(CorusPageIndex.is_base_template == True).order(
            -CorusPageIndex.updated).fetch()
        _base_futs = []  # These had better all exist, skipping error checking
        for b in _bases:
            _base_futs.append(CorusPageVersion.get_by_id_async(
                "%s:%i" % (b.key.id(), b.published_versions[0])))
        for fut in _base_futs:
            fut = fut.get_result()
            base_templates[fut.key.id().split(':')[0]] = fut.title
        return base_templates

    def new_page_endpoint(self, path, base_template, title, content, notes=''):
        """
        Create a new page and a new starting version
        TODO:
            Throw new page and version into search doc
            Default things better based on the base template:
                - Give a new default full page
                - Give a simple page template based on blocks (maybe make this tricky or
                  configurable
        """
        path = PageService._sanitize_path(path)
        idx = CorusPageIndex.get_by_id(path)
        if idx:
            raise ValueError("Path (%s) already exists" % path)

        self._create_new_page(path, base_template, title, content, notes)
        return '/cor/console/pages/edit?path=' + str(path)

    def new_version_endpoint(self, path, base_template, title, content, publish, revision_notes=''):
        """
        Create new page version
        TODO:
            Throw new page and version into search doc
        """
        path = PageService._sanitize_path(path)
        idx = CorusPageIndex.get_by_id(path)
        idx.number_of_versions += 1
        if publish:
            idx.published_versions = [idx.number_of_versions]

        version = CorusPageVersion(id=path + ':%i' % idx.number_of_versions,
                                   title=title.strip(),
                                   content=content.strip(),
                                   base_template=base_template.strip(),
                                   private_revision_notes=revision_notes)
        self._put_page(idx, version)
        return '/cor/console/pages/edit?path=' + str(path)
