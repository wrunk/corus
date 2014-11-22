#!/usr/bin/env python


import logging


_log = logging.getLogger(__name__)

# TODO finish and use this
class HandleError(object):
    """
    Nudge error handler for use with html pages
    """
    code = 500
    content_type = 'text/html; charset=utf-8'
    content = '<html></body><p>Error</p></body></html>'
    # content = registry.template_env.get_template('generic_message.html').render(
    #     title='Oops an error occurred',
    #     message='A server error has occurred. Please try again, or use the links at the top to chose another page.'
    # ).encode('utf8')
    headers = {}

    def __call__(self, exp, req):
        if hasattr(exp, 'http_status_code'):
            self.code = exp.http_status_code
            self.content = '<html></body><p>Error</p></body></html>'
            # self.content = registry.template_env.get_template('generic_message.html').render(
            #     title=exp.http_title, message=exp.http_message
            # ).encode('utf8')

        # Return the default generic page
        return self.code, self.content_type, self.content, self.headers