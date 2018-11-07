"""
WSGI config for bonds project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
if os.environ.get('ENVIRONMENT_NAME') == 'development':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bonds.settings.settings-dev")
else:
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bonds.settings.settings-prod")

application = get_wsgi_application()
