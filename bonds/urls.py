"""bonds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse


urlpatterns = [
    ## Force page to go to admin site
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(
        r'^login/$',
        login,
        {
            'template_name': 'admin/login.html',
            'extra_context': {
                # Your extra variables here as key value pairs.
                'title': getattr(settings, 'LOGIN_HEADER'),
                'debug': getattr(settings, 'DEBUG')
            }
        },
        name='login'
    ),
    url(r'^report_builder/', include('report_builder.urls')),
    url(
        r'^admin/login/$',
        login,
        {
            'template_name': 'admin/login.html',
            'extra_context': {
                # Your extra variables here as key value pairs.
                'title': getattr(settings, 'LOGIN_HEADER')
            }
        },
        name='login'
    ),
    url(r'^admin/', admin.site.urls),
]
