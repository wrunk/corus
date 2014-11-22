"""
Very basic django-style settings.


"""

from nudge.json import ObjDict


settings = ObjDict({
    # The domain name the site will use. Can just be <my-app-engine-proj>.appspot.com
    'site_host': '',
    # Need this for email redirecting (maybe)
    'local_dev_port': 8095,

})