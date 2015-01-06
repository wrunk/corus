"""
Very basic django-style settings.


"""

from nudge.json import ObjDict


settings = ObjDict({
    # The domain name the site will use. Can just be <my-app-engine-proj>.appspot.com
    'site_host': '',

    # Need this for email redirecting (maybe)
    'local_dev_port': 8095,

    # Where the corus page generator starts from
    'pages_root_path': '/',

    # Auth token
    'app_key': '',

    # Site templates root
    'templates_root': 'templates',

    # Base templates dir must be *within* templates_root for now
    'base_templates_dir': 'base',
})