from config.settings import *
from django.conf import settings

# Debug Toolbar
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: settings.DEBUG}
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
